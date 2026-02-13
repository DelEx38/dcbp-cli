"""
DCBP CLI - Implementation des commandes.
"""

import shutil
import sys
from pathlib import Path
from importlib import resources

from . import __version__


def get_templates_path() -> Path:
    """Retourne le chemin vers les templates inclus dans le package."""
    try:
        # Python 3.9+
        return resources.files("dcbp_cli") / "templates"
    except AttributeError:
        # Python 3.8 fallback
        import pkg_resources
        return Path(pkg_resources.resource_filename("dcbp_cli", "templates"))


def init_project(project_path: Path, force: bool = False) -> bool:
    """
    Initialise DCBP dans un projet.

    Args:
        project_path: Chemin du projet cible
        force: Si True, ecrase les fichiers existants

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

    print(f"[*] Initialisation de DCBP v{__version__} dans {project_path}")
    print()

    # Copier le dossier .dcbp
    dcbp_template = templates_path / ".dcbp"
    if dcbp_template.exists():
        if dcbp_path.exists() and force:
            shutil.rmtree(dcbp_path)
        shutil.copytree(dcbp_template, dcbp_path)
        print("[+] Cree .dcbp/")

    # Copier CLAUDE.md
    claude_template = templates_path / "CLAUDE.md"
    if claude_template.exists():
        if claude_md.exists() and not force:
            print("[!] CLAUDE.md existe deja (ignore)")
        else:
            shutil.copy2(claude_template, claude_md)
            print("[+] Cree CLAUDE.md")

    print()
    print("=" * 50)
    print("[OK] DCBP initialise avec succes!")
    print("=" * 50)
    print()
    print("Prochaines etapes:")
    print("  1. Editez .dcbp/PROJECT.md avec les infos de votre projet")
    print("  2. Utilisez /dev <feature> pour demarrer un developpement")
    print()
    print("Skills disponibles:")
    print("  /dev <feature>   - Developpement structure")
    print("  /debug <bug>     - Investigation de bugs")
    print("  /review <cible>  - Revue de code")
    print("  /status          - Vue d'ensemble du projet")
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
    ]

    # Mettre a jour les skills
    skills_src = templates_path / ".dcbp" / "skills"
    skills_dst = dcbp_path / "skills"

    if skills_src.exists():
        if skills_dst.exists():
            shutil.rmtree(skills_dst)
        shutil.copytree(skills_src, skills_dst)
        print("[+] Mis a jour skills/")

    # Mettre a jour les scripts
    scripts_src = templates_path / ".dcbp" / "scripts"
    scripts_dst = dcbp_path / "scripts"

    if scripts_src.exists():
        if scripts_dst.exists():
            shutil.rmtree(scripts_dst)
        shutil.copytree(scripts_src, scripts_dst)
        print("[+] Mis a jour scripts/")

    print()
    print("[OK] Templates mis a jour!")
    print()
    print("Fichiers preserves:")
    for f in preserve:
        if (dcbp_path / f).exists():
            print(f"  [+] {f}")
    print()

    return True
