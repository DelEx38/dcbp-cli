"""
DCBP CLI - Implementation des commandes.
"""

import shutil
import sys
from pathlib import Path
from importlib import resources
from datetime import date

from . import __version__


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
        force: Si True, ecrase les fichiers existants
        skip_questions: Si True, ne pose pas de questions (mode rapide)

    Returns:
        True si succes, False sinon
    """
    project_path = project_path.resolve()
    dcbp_path = project_path / ".dcbp"
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

    # Copier le dossier .dcbp
    dcbp_template = templates_path / ".dcbp"
    if dcbp_template.exists():
        if dcbp_path.exists() and force:
            shutil.rmtree(dcbp_path)
        shutil.copytree(dcbp_template, dcbp_path)
        print("[+] Cree .dcbp/")

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

    # Copier le dossier .claude/skills (format natif Claude Code)
    # 1. Dans le projet local
    claude_template = templates_path / ".claude"
    claude_path = project_path / ".claude"
    if claude_template.exists():
        if claude_path.exists() and force:
            shutil.rmtree(claude_path)
        if not claude_path.exists():
            shutil.copytree(claude_template, claude_path)
            skills_dirs = [d.name for d in (claude_path / "skills").iterdir() if d.is_dir()]
            print(f"[+] Cree .claude/skills/ ({', '.join(sorted(skills_dirs))})")

    # 2. Dans le dossier global ~/.claude/skills/ (pour que les skills soient toujours disponibles)
    home_claude_path = Path.home() / ".claude"
    home_skills_path = home_claude_path / "skills"
    skills_template = templates_path / ".claude" / "skills"
    if skills_template.exists():
        home_claude_path.mkdir(exist_ok=True)
        if home_skills_path.exists() and force:
            shutil.rmtree(home_skills_path)
        if not home_skills_path.exists():
            shutil.copytree(skills_template, home_skills_path)
            skills_dirs = [d.name for d in home_skills_path.iterdir() if d.is_dir()]
            print(f"[+] Cree ~/.claude/skills/ ({', '.join(sorted(skills_dirs))})")
        else:
            # Copier les skills manquants sans écraser
            for skill_dir in skills_template.iterdir():
                if skill_dir.is_dir():
                    dest_skill = home_skills_path / skill_dir.name
                    if not dest_skill.exists():
                        shutil.copytree(skill_dir, dest_skill)
                        print(f"    [+] Ajoute skill: {skill_dir.name}")
                    elif force:
                        shutil.rmtree(dest_skill)
                        shutil.copytree(skill_dir, dest_skill)
                        print(f"    [*] Mis a jour: {skill_dir.name}")

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
    dcbp_path = project_path / ".dcbp"

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
    claude_skills_src = templates_path / ".claude" / "skills"
    claude_path = project_path / ".claude"
    claude_skills_dst = claude_path / "skills"

    if claude_skills_src.exists():
        if not claude_path.exists():
            claude_path.mkdir()
        if claude_skills_dst.exists():
            shutil.rmtree(claude_skills_dst)
        shutil.copytree(claude_skills_src, claude_skills_dst)
        skills_dirs = [d.name for d in claude_skills_dst.iterdir() if d.is_dir()]
        print(f"[+] Mis a jour .claude/skills/ ({', '.join(sorted(skills_dirs))})")

    # Mettre a jour les skills (~/.claude/skills/) - global
    home_claude_path = Path.home() / ".claude"
    home_skills_path = home_claude_path / "skills"

    if claude_skills_src.exists():
        home_claude_path.mkdir(exist_ok=True)
        if home_skills_path.exists():
            shutil.rmtree(home_skills_path)
        shutil.copytree(claude_skills_src, home_skills_path)
        skills_dirs = [d.name for d in home_skills_path.iterdir() if d.is_dir()]
        print(f"[+] Mis a jour ~/.claude/skills/ ({', '.join(sorted(skills_dirs))})")

    # Mettre a jour les scripts
    scripts_src = templates_path / ".dcbp" / "scripts"
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
