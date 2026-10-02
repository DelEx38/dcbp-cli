#!/usr/bin/env python3
"""
DCBP CLI - Point d'entrée principal.

Usage:
    dcbp init [--force] [--quick]
    dcbp update
    dcbp --version
    dcbp --help
"""

import argparse
import sys
from pathlib import Path

from . import __version__
from .commands import init_project, update_templates


def main():
    """Point d'entrée CLI principal."""
    parser = argparse.ArgumentParser(
        prog="dcbp",
        description="DC Blueprint - Système de mémoire persistante pour Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  dcbp init          Initialise DCBP avec questions interactives
  dcbp init --quick  Initialise sans questions (templates par défaut)
  dcbp init --force  Réinitialise (écrase les fichiers DCBP existants)
  dcbp update        Met à jour les templates vers la dernière version
        """
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"dcbp-cli {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # Commande init
    init_parser = subparsers.add_parser(
        "init",
        help="Initialise DCBP dans le projet courant"
    )
    init_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Écrase les fichiers existants"
    )
    init_parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Mode rapide sans questions (utilise les templates par défaut)"
    )
    init_parser.add_argument(
        "--path", "-p",
        type=str,
        default=".",
        help="Chemin du projet (défaut: répertoire courant)"
    )

    # Commande update
    update_parser = subparsers.add_parser(
        "update",
        help="Met à jour les templates DCBP"
    )
    update_parser.add_argument(
        "--path", "-p",
        type=str,
        default=".",
        help="Chemin du projet (défaut: répertoire courant)"
    )

    # Commande doctor
    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Vérifie l'état d'un projet DCBP (read-only)"
    )
    doctor_parser.add_argument(
        "--path", "-p",
        type=str,
        default=".",
        help="Chemin du projet (défaut: répertoire courant)"
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "init":
        success = init_project(
            Path(args.path),
            force=args.force,
            skip_questions=args.quick
        )
        sys.exit(0 if success else 1)

    elif args.command == "update":
        success = update_templates(Path(args.path))
        sys.exit(0 if success else 1)

    elif args.command == "doctor":
        from .doctor import run_checks, print_doctor_result
        result = run_checks(Path(args.path))
        print_doctor_result(result)
        sys.exit(result.exit_code)

if __name__ == "__main__":
    main()
