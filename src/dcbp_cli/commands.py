"""
DCBP CLI - Implementation des commandes.
"""

import shutil
import sys
from pathlib import Path
from importlib import resources
from datetime import date

from . import __version__


# ============================================================================
# Ownership model
# ============================================================================

import hashlib
from enum import Enum


class Ownership(Enum):
    OWNED = "owned"
    UNKNOWN = "unknown"


# Skills shipped by DCBP v0.5.0 (12 skills)
DCBP_KNOWN_SKILL_NAMES: frozenset = frozenset({
    "archive", "bugfix", "commit", "deploy", "dev", "docs",
    "etat", "logs", "refactor", "review", "start", "test",
    # Historical names (pre-v0.5.0)
    "debug", "status", "create",
})

# Text that only appears in DCBP-specific skills (not generic ones)
DCBP_SPECIFIC_MARKERS: tuple = (
    ".claude/dcbp/",
    "SESSION DCBP INITIALISÉE",
    "ARCHIVAGE TERMINÉ",
    "Vue d'ensemble rapide du projet DCBP",
)

# SHA-256 hashes of known DCBP v0.5.0 SKILL.md files (content with LF line endings)
# Computed from src/dcbp_cli/templates/.claude/skills/*/SKILL.md BEFORE adding tool: dcbp
DCBP_V050_SKILL_HASHES: dict = {
    "archive": "11ef301cbdeeb47baccd5aa16a3eb25802f32c75e4318df70b2355ce75b3b59b",
    "bugfix": "d5d495844933f33ae30ff72c482fcd2631ceb09a005dddaf59e1eac5909cef0e",
    "commit": "fa6ac90216608882d0232c219f3f96c1faf923d6a010a5aacd6f758e366df6a2",
    "deploy": "e4b0d03a2b6216119bd86119ce01169660f9fedd84cc4d7eb2ee2eb98a1c3107",
    "dev": "cfa8e99f42ed4587ee1920521efd82bc58b7217328f932ef7325efea903b8009",
    "docs": "572080817d60e755eaf7e78371f2b5aeb195e745c8ce6284315c2e5e1469de82",
    "etat": "d23482a761153f9bf877af41f7064d30356459d3baa4267404e1f138133ee412",
    "logs": "17d3f49dffcfe5f6f7e53f7e39b434eea11ac10c4606fcbbf38e4eecd6e183db",
    "refactor": "46f3e68ddcb8cc2ddde68462d38ff6bde8ba09bec4beede0bfcea44d8c05262d",
    "review": "f0d60bcbe75861d11df26c5addf32c1a7b5454e482469723446cf6acf697fc86",
    "start": "b09a623384c34a9c603eb367d6bf057183e8b1088e5f9f7f58a53c7ea3b9c4c4",
    "test": "8ba39f7f9988bbe4a2409a9ca06fcaf76cd72a62cad3d6751709421d70eba149",
}


def _parse_frontmatter(content: str) -> dict | None:
    """
    Parse YAML frontmatter from a SKILL.md file.
    Returns the frontmatter dict, or None if no valid frontmatter found.
    Frontmatter is delimited by --- on the first and second line.
    Only parses the frontmatter block, never the body.
    """
    lines = content.split('\n')
    if not lines or lines[0].strip() != '---':
        return None

    # Find closing ---
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end_idx = i
            break

    if end_idx is None:
        return None

    # Parse frontmatter lines as simple key: value
    # Avoid adding yaml dependency - parse manually for our limited use case
    frontmatter = {}
    for line in lines[1:end_idx]:
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip().strip('"\'')
            if key:
                frontmatter[key] = value

    return frontmatter


def classify_skill(skill_dir: Path) -> Ownership:
    """
    Classify a skill directory as OWNED or UNKNOWN.
    Conservative: returns UNKNOWN for any ambiguous case.
    Never bases classification solely on directory name.
    """
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return Ownership.UNKNOWN

    try:
        content_raw = skill_md.read_bytes()
    except (OSError, PermissionError, IsADirectoryError):
        return Ownership.UNKNOWN

    # Normalize line endings for comparison
    content_normalized = content_raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    content_str = content_normalized.decode('utf-8', errors='replace')

    # Criterion 1: Explicit ownership marker in FRONTMATTER (not body)
    # Requires full identity coherence: tool==dcbp AND name==dir_name AND name in catalog
    fm = _parse_frontmatter(content_str)
    if fm is not None and fm.get('tool', '').lower() == 'dcbp':
        fm_name = fm.get('name', '').strip()
        dir_name = skill_dir.name
        if fm_name == dir_name and dir_name in DCBP_KNOWN_SKILL_NAMES:
            return Ownership.OWNED
        # Incoherent identity (name mismatch or unknown catalog entry) → UNKNOWN
        return Ownership.UNKNOWN

    # Criterion 2: Hash match against known v0.5.0 templates + DCBP-specific text
    content_hash = hashlib.sha256(content_normalized).hexdigest()
    skill_name = skill_dir.name

    expected_hash = DCBP_V050_SKILL_HASHES.get(skill_name)
    hash_matches = expected_hash is not None and expected_hash == content_hash
    has_dcbp_marker = any(marker in content_str for marker in DCBP_SPECIFIC_MARKERS)

    if hash_matches and has_dcbp_marker:
        return Ownership.OWNED

    # Everything else is UNKNOWN
    return Ownership.UNKNOWN


def _install_skills_to_project(
    skills_src: Path,
    skills_dst: Path,
    force: bool = False,
) -> dict:
    """
    Install DCBP skills into {project}/.claude/skills/ skill by skill.
    Never removes the destination directory.
    Never overwrites UNKNOWN skills.
    Returns report dict with installed/updated/skipped lists.
    """
    if not skills_src.exists():
        return {"installed": [], "updated": [], "skipped_unknown": [], "skipped_existing": []}

    skills_dst.mkdir(parents=True, exist_ok=True)

    installed = []
    updated = []
    skipped_unknown = []
    skipped_existing = []

    for skill_src_dir in sorted(skills_src.iterdir()):
        if not skill_src_dir.is_dir():
            continue

        skill_name = skill_src_dir.name
        skill_dest_dir = skills_dst / skill_name

        if not skill_dest_dir.exists():
            shutil.copytree(skill_src_dir, skill_dest_dir)
            installed.append(skill_name)
        else:
            ownership = classify_skill(skill_dest_dir)
            if ownership == Ownership.OWNED:
                if force:
                    shutil.rmtree(skill_dest_dir)
                    shutil.copytree(skill_src_dir, skill_dest_dir)
                    updated.append(skill_name)
                else:
                    skipped_existing.append(skill_name)
            else:
                skipped_unknown.append(skill_name)
                print(f"    [!] Conservé (propriété inconnue) : {skill_name}/")

    return {
        "installed": installed,
        "updated": updated,
        "skipped_unknown": skipped_unknown,
        "skipped_existing": skipped_existing,
    }


def migrate_global_skills(home_skills_path: Path) -> dict:
    """
    Remove only DCBP-owned skills from ~/.claude/skills/.
    Conservative: UNKNOWN elements are NEVER touched.
    Idempotent: safe to call multiple times.
    """
    if not home_skills_path.exists():
        return {"removed": [], "unknown": [], "not_dir": []}

    removed = []
    unknown = []
    not_dir = []

    for entry in sorted(home_skills_path.iterdir()):
        if not entry.is_dir():
            not_dir.append(entry.name)
            continue

        ownership = classify_skill(entry)

        if ownership == Ownership.OWNED:
            shutil.rmtree(entry)
            removed.append(entry.name)
        else:
            unknown.append(entry.name)

    return {"removed": removed, "unknown": unknown, "not_dir": not_dir}


def _print_migration_report(report: dict, home_skills_path: Path) -> None:
    """Print a user-friendly migration report."""
    if not report["removed"] and not report["unknown"]:
        return  # Nothing to report if no global skills at all

    print()
    print("[*] Vérification des anciens skills globaux dans ~/.claude/skills/")

    if report["removed"]:
        print(f"[+] Retirés (identifiés DCBP) : {', '.join(report['removed'])}")

    if report["unknown"]:
        print(f"[?] Conservés (propriété inconnue) : {', '.join(report['unknown'])}")
        print("    Ces éléments n'ont pas été modifiés.")
        print("    Si certains proviennent d'une ancienne installation DCBP,")
        print("    vous pouvez les supprimer manuellement.")

    if not report["removed"]:
        print("    Aucun skill DCBP identifiable avec certitude.")
        print("    Rien n'a été modifié.")


# =============================================================================
# Configuration des choix
# =============================================================================

LANGUAGES = {
    "1": {"name": "Python", "key": "python"},
    "2": {"name": "JavaScript/TypeScript", "key": "javascript"},
    "3": {"name": "Go", "key": "go"},
    "4": {"name": "Rust", "key": "rust"},
    "5": {"name": "Autre", "key": "other"},
}

FRAMEWORKS = {
    "python": {
        "1": "FastAPI",
        "2": "Django",
        "3": "Flask",
        "4": "CLI (Click/Typer)",
        "5": "Script simple",
        "6": "Autre",
    },
    "javascript": {
        "1": "React",
        "2": "Next.js",
        "3": "Vue.js",
        "4": "Node.js (Express)",
        "5": "Autre",
    },
    "go": {
        "1": "Gin",
        "2": "Echo",
        "3": "Fiber",
        "4": "CLI (Cobra)",
        "5": "Autre",
    },
    "rust": {
        "1": "Actix-web",
        "2": "Axum",
        "3": "Rocket",
        "4": "CLI (Clap)",
        "5": "Autre",
    },
    "other": {
        "1": "Aucun / Autre",
    },
}

DATABASES = {
    "1": "PostgreSQL",
    "2": "MySQL",
    "3": "SQLite",
    "4": "MongoDB",
    "5": "Redis",
    "6": "Aucune",
    "7": "Autre",
}

TOOLS = {
    "python": {
        "test": "pytest",
        "lint": "ruff",
        "format": "ruff format",
        "typecheck": "mypy",
    },
    "javascript": {
        "test": "jest / vitest",
        "lint": "eslint",
        "format": "prettier",
        "typecheck": "tsc (si TypeScript)",
    },
    "go": {
        "test": "go test",
        "lint": "golangci-lint",
        "format": "gofmt",
        "typecheck": "(intégré)",
    },
    "rust": {
        "test": "cargo test",
        "lint": "clippy",
        "format": "rustfmt",
        "typecheck": "(intégré)",
    },
    "other": {
        "test": "[À configurer]",
        "lint": "[À configurer]",
        "format": "[À configurer]",
        "typecheck": "[À configurer]",
    },
}


# =============================================================================
# Fonctions utilitaires
# =============================================================================

def get_templates_path() -> Path:
    """Retourne le chemin vers les templates inclus dans le package."""
    try:
        # Python 3.9+
        return resources.files("dcbp_cli") / "templates"
    except AttributeError:
        # Python 3.8 fallback
        import pkg_resources
        return Path(pkg_resources.resource_filename("dcbp_cli", "templates"))


def is_interactive() -> bool:
    """Vérifie si le terminal est interactif."""
    import sys
    return sys.stdin.isatty()


def ask_text(prompt: str, default: str = "") -> str:
    """Demande une saisie texte."""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "

    try:
        response = input(prompt).strip()
        return response if response else default
    except (EOFError, KeyboardInterrupt):
        print()  # Nouvelle ligne
        return default


def ask_choice(prompt: str, choices: dict, default: str = "1") -> str:
    """Demande un choix parmi plusieurs options."""
    print(f"\n{prompt}")
    for key, value in choices.items():
        if isinstance(value, dict):
            print(f"  {key}. {value['name']}")
        else:
            print(f"  {key}. {value}")

    try:
        while True:
            response = input(f"Choix [{default}]: ").strip()
            if not response:
                response = default
            if response in choices:
                return response
            print(f"  [!] Choix invalide. Entrez un numero entre 1 et {len(choices)}")
    except (EOFError, KeyboardInterrupt):
        print()  # Nouvelle ligne
        return default


def generate_project_md(config: dict) -> str:
    """Génère le contenu de PROJECT.md basé sur la configuration."""
    tools = TOOLS.get(config["language_key"], TOOLS["other"])

    content = f"""# {config['name']}

> {config['description']}

## Informations générales

- **Nom** : {config['name']}
- **Description** : {config['description']}
- **Démarré le** : {date.today().isoformat()}

## Stack technique

### Langage
- {config['language']}

### Framework
- {config['framework']}

### Base de données
- {config['database']}

### Outils
- **Tests** : {tools['test']}
- **Linter** : {tools['lint']}
- **Formatter** : {tools['format']}
- **Type check** : {tools['typecheck']}

## Architecture

### Structure
```
{config['name'].lower().replace(' ', '_')}/
├── src/
├── tests/
└── ...
```

### Patterns
- [À compléter selon le projet]

## Conventions

### Nommage
- Variables : `snake_case`
- Classes : `PascalCase`
- Fichiers : `snake_case`

### Style
- Formatter : {tools['format']}
- Linter : {tools['lint']}

### Tests
- Framework : {tools['test']}
- Convention : `test_<fonction>_<scenario>`

## Validation

Commandes à exécuter pour valider le code :

```bash
# Lint
{_get_lint_command(config['language_key'], tools)}

# Type check
{_get_typecheck_command(config['language_key'], tools)}

# Tests
{_get_test_command(config['language_key'], tools)}
```

## Points d'attention

### À faire systématiquement
- Écrire des tests pour les nouvelles fonctionnalités
- Documenter les fonctions publiques
- Vérifier les types avant de commit

### À éviter
- Commit de fichiers sensibles (.env, credentials)
- Code dupliqué sans refactoring
- Fonctions trop longues (> 50 lignes)

### Zones sensibles
- [À compléter selon le projet]
"""
    return content


def _get_lint_command(lang_key: str, tools: dict) -> str:
    """Retourne la commande de lint selon le langage."""
    commands = {
        "python": "ruff check .",
        "javascript": "npm run lint",
        "go": "golangci-lint run",
        "rust": "cargo clippy",
        "other": "# [À configurer]",
    }
    return commands.get(lang_key, commands["other"])


def _get_typecheck_command(lang_key: str, tools: dict) -> str:
    """Retourne la commande de type check selon le langage."""
    commands = {
        "python": "mypy src/",
        "javascript": "npx tsc --noEmit",
        "go": "# (intégré au compilateur)",
        "rust": "# (intégré au compilateur)",
        "other": "# [À configurer]",
    }
    return commands.get(lang_key, commands["other"])


def _get_test_command(lang_key: str, tools: dict) -> str:
    """Retourne la commande de test selon le langage."""
    commands = {
        "python": "pytest",
        "javascript": "npm test",
        "go": "go test ./...",
        "rust": "cargo test",
        "other": "# [À configurer]",
    }
    return commands.get(lang_key, commands["other"])


# =============================================================================
# Commandes principales
# =============================================================================

def init_project(project_path: Path, force: bool = False, skip_questions: bool = False) -> bool:
    """
    Initialise DCBP dans un projet.

    Args:
        project_path: Chemin du projet cible
        force: Si True, ecrase les fichiers existants DCBP (jamais les skills inconnus)
        skip_questions: Si True, ne pose pas de questions (mode rapide)

    Returns:
        True si succes, False sinon
    """
    project_path = project_path.resolve()
    claude_path = project_path / ".claude"
    dcbp_path = claude_path / "dcbp"
    claude_md = project_path / "CLAUDE.md"

    # Verifier si deja initialise
    if dcbp_path.exists() and not force:
        print(f"[!] DCBP deja initialise dans {project_path}")
        print("    Utilisez --force pour reinitialiser")
        return False

    templates_path = get_templates_path()

    if not templates_path.exists():
        print(f"[X] Templates non trouves: {templates_path}")
        return False

    print()
    print("=" * 60)
    print(f"  DCBP v{__version__} - Initialisation du projet")
    print("=" * 60)
    print()

    # Configuration du projet
    config = {}

    # Vérifier si l'environnement est interactif
    if not skip_questions and not is_interactive():
        print("[!] Terminal non-interactif detecte, mode --quick active")
        print()
        skip_questions = True

    if not skip_questions:
        print("Repondez aux questions suivantes pour configurer votre projet.")
        print("(Appuyez sur Entree pour accepter la valeur par defaut)")
        print()

        # Nom du projet
        default_name = project_path.name
        config["name"] = ask_text("Nom du projet", default_name)

        # Description
        config["description"] = ask_text("Description courte", "Un projet genial")

        # Langage
        lang_choice = ask_choice("Langage principal ?", LANGUAGES)
        config["language"] = LANGUAGES[lang_choice]["name"]
        config["language_key"] = LANGUAGES[lang_choice]["key"]

        # Framework
        frameworks = FRAMEWORKS.get(config["language_key"], FRAMEWORKS["other"])
        framework_choice = ask_choice(f"Framework {config['language']} ?", frameworks)
        config["framework"] = frameworks[framework_choice]

        # Base de données
        db_choice = ask_choice("Base de donnees ?", DATABASES, default="6")
        config["database"] = DATABASES[db_choice]

        print()
    else:
        # Mode rapide sans questions
        config = {
            "name": project_path.name,
            "description": "Un projet DCBP",
            "language": "[À configurer]",
            "language_key": "other",
            "framework": "[À configurer]",
            "database": "[À configurer]",
        }

    # Copier les templates
    print("[*] Creation de la structure DCBP...")
    print()

    # Creer le dossier .claude s'il n'existe pas
    claude_path.mkdir(exist_ok=True)

    # Copier le dossier dcbp dans .claude/dcbp
    dcbp_template = templates_path / ".claude" / "dcbp"
    if dcbp_template.exists():
        if dcbp_path.exists() and force:
            shutil.rmtree(dcbp_path)
        if not dcbp_path.exists():
            shutil.copytree(dcbp_template, dcbp_path)
        print("[+] Cree .claude/dcbp/")

        # Lister les composants crees
        if (dcbp_path / "skills").exists():
            skills = [d.name for d in (dcbp_path / "skills").iterdir() if d.is_dir()]
            if skills:
                print(f"    [+] Skills: {', '.join(sorted(skills))}")

        if (dcbp_path / "scripts").exists():
            print("    [+] Scripts utilitaires")

        if (dcbp_path / "output").exists():
            print("    [+] Dossier output/")

        if (dcbp_path / "archive").exists():
            print("    [+] Dossier archive/")

    # Installer les skills dans .claude/skills/ (format natif Claude Code)
    # Uses skill-by-skill installation: NEVER overwrites UNKNOWN skills
    skills_template = templates_path / ".claude" / "skills"
    skills_path = claude_path / "skills"
    if skills_template.exists():
        report = _install_skills_to_project(skills_template, skills_path, force=force)
        if report["installed"]:
            print(f"[+] Skills installes : {', '.join(sorted(report['installed']))}")
        if report["updated"]:
            print(f"[*] Skills mis a jour : {', '.join(sorted(report['updated']))}")
        if report["skipped_unknown"]:
            print(f"[!] Skills conserves (inconnus) : {', '.join(sorted(report['skipped_unknown']))}")

    # Migrate: clean up DCBP-owned skills from ~/.claude/skills/ if present
    home_skills_path = Path.home() / ".claude" / "skills"
    migration_report = migrate_global_skills(home_skills_path)
    _print_migration_report(migration_report, home_skills_path)

    # Copier CLAUDE.md
    claude_template = templates_path / "CLAUDE.md"
    if claude_template.exists():
        if claude_md.exists() and not force:
            print("[!] CLAUDE.md existe deja (ignore)")
        else:
            shutil.copy2(claude_template, claude_md)
            print("[+] Cree CLAUDE.md")

    # Générer PROJECT.md personnalisé
    if not skip_questions:
        project_md_content = generate_project_md(config)
        project_md_path = dcbp_path / "PROJECT.md"
        project_md_path.write_text(project_md_content, encoding="utf-8")
        print("[+] Configure PROJECT.md")

    print()
    print("=" * 60)
    print("  [OK] DCBP initialise avec succes!")
    print("=" * 60)
    print()

    if not skip_questions:
        print(f"  Projet    : {config['name']}")
        print(f"  Langage   : {config['language']}")
        print(f"  Framework : {config['framework']}")
        print(f"  Database  : {config['database']}")
        print()

    print("Prochaines etapes:")
    print("  1. Lancez Claude Code dans ce dossier")
    print("  2. Utilisez /start pour initialiser votre session")
    print("  3. Utilisez /dev <feature> pour developper")
    print()
    print("Skills disponibles:")
    print("  /start                  - Initialiser une session")
    print("  /dev <feature>          - Developpement structure")
    print("  /bugfix <bug>           - Investigation de bugs")
    print("  /review <cible>         - Revue de code")
    print("  /etat                   - Vue d'ensemble du projet")
    print("  /archive                - Archiver PROGRESS.md")
    print()

    return True


def update_templates(project_path: Path) -> bool:
    """
    Met a jour les templates DCBP sans ecraser la memoire.

    Args:
        project_path: Chemin du projet cible

    Returns:
        True si succes, False sinon
    """
    project_path = project_path.resolve()
    claude_path = project_path / ".claude"
    dcbp_path = claude_path / "dcbp"

    if not dcbp_path.exists():
        print("[X] DCBP non initialise dans ce projet")
        print("    Executez d'abord: dcbp init")
        return False

    templates_path = get_templates_path()

    print(f"[*] Mise a jour des templates DCBP vers v{__version__}")
    print()

    # Fichiers a preserver (memoire du projet)
    preserve = [
        "PROJECT.md",
        "PROGRESS.md",
        "TASKS.md",
        "ISSUES.md",
        "DECISIONS.md",
        "output",
        "archive",
    ]

    # Mettre a jour les skills (.claude/skills/) - local
    # Uses skill-by-skill update with force=True for OWNED skills
    # NEVER overwrites UNKNOWN skills
    claude_skills_src = templates_path / ".claude" / "skills"
    claude_skills_dst = claude_path / "skills"

    if claude_skills_src.exists():
        report = _install_skills_to_project(claude_skills_src, claude_skills_dst, force=True)
        all_touched = report["installed"] + report["updated"]
        if all_touched:
            print(f"[+] Mis a jour .claude/skills/ ({', '.join(sorted(all_touched))})")
        if report["skipped_unknown"]:
            print(f"[!] Conserves (inconnus) : {', '.join(sorted(report['skipped_unknown']))}")

    # Migrate: clean up DCBP-owned skills from ~/.claude/skills/ if present
    home_skills_path = Path.home() / ".claude" / "skills"
    migration_report = migrate_global_skills(home_skills_path)
    _print_migration_report(migration_report, home_skills_path)

    # Mettre a jour les scripts
    scripts_src = templates_path / ".claude" / "dcbp" / "scripts"
    scripts_dst = dcbp_path / "scripts"

    if scripts_src.exists():
        if scripts_dst.exists():
            shutil.rmtree(scripts_dst)
        shutil.copytree(scripts_src, scripts_dst)
        print("[+] Mis a jour scripts/")

    # S'assurer que le dossier archive existe
    archive_dst = dcbp_path / "archive"
    if not archive_dst.exists():
        archive_dst.mkdir()
        (archive_dst / ".gitkeep").touch()
        print("[+] Cree archive/")

    print()
    print("[OK] Templates mis a jour!")
    print()
    print("Fichiers preserves:")
    for f in preserve:
        if (dcbp_path / f).exists():
            print(f"  [+] {f}")
    print()

    return True
