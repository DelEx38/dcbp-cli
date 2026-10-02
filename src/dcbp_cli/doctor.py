"""
DCBP Doctor — read-only deterministic project health check.

Never modifies any file. Never creates any file. Never calls dcbp init/update.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from . import __version__
from .contract import CORE_SKILL_NAMES, LEGACY_SCRIPT_NAMES
from .commands import classify_skill, Ownership

Status = Literal["PASS", "WARNING", "ERROR"]

# Fixed check IDs for core skills (alphabetical order of CORE_SKILL_NAMES)
_CORE_SKILL_IDS: dict[str, str] = {
    "archive": "D09",
    "bugfix":  "D10",
    "dev":     "D11",
    "etat":    "D12",
    "review":  "D13",
    "start":   "D14",
}


@dataclass
class CheckResult:
    id: str
    name: str
    status: Status
    message: str


@dataclass
class DoctorResult:
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def errors(self) -> list[CheckResult]:
        return [c for c in self.checks if c.status == "ERROR"]

    @property
    def warnings(self) -> list[CheckResult]:
        return [c for c in self.checks if c.status == "WARNING"]

    @property
    def passes(self) -> list[CheckResult]:
        return [c for c in self.checks if c.status == "PASS"]

    @property
    def exit_code(self) -> int:
        if self.errors:
            return 2
        if self.warnings:
            return 1
        return 0


def run_checks(project_path: Path) -> DoctorResult:
    """Run all Doctor checks on project_path. Strictly read-only."""
    project_path = project_path.resolve()
    checks = []

    dcbp_path = project_path / ".claude" / "dcbp"

    # ── ESSENTIAL — ERROR if absent ────────────────────────────────────────

    if dcbp_path.exists() and dcbp_path.is_dir():
        checks.append(CheckResult("D01", "Project memory dir", "PASS",
            ".claude/dcbp/ présent"))
    else:
        checks.append(CheckResult("D01", "Project memory dir", "ERROR",
            "DCBP non initialisé dans ce projet. Exécutez: dcbp init"))

    project_md = dcbp_path / "PROJECT.md"
    if project_md.is_file():
        try:
            project_md.read_bytes()
            checks.append(CheckResult("D02", "PROJECT.md", "PASS", "Présent et lisible"))
        except (OSError, PermissionError):
            checks.append(CheckResult("D02", "PROJECT.md", "ERROR",
                "PROJECT.md illisible"))
    else:
        checks.append(CheckResult("D02", "PROJECT.md", "ERROR",
            ".claude/dcbp/PROJECT.md manquant"))

    progress_md = dcbp_path / "PROGRESS.md"
    if progress_md.is_file():
        try:
            progress_md.read_bytes()
            checks.append(CheckResult("D03", "PROGRESS.md", "PASS", "Présent et lisible"))
        except (OSError, PermissionError):
            checks.append(CheckResult("D03", "PROGRESS.md", "ERROR",
                "PROGRESS.md illisible"))
    else:
        checks.append(CheckResult("D03", "PROGRESS.md", "ERROR",
            ".claude/dcbp/PROGRESS.md manquant"))

    # ── EXPECTED — WARNING if absent ───────────────────────────────────────

    claude_md = project_path / "CLAUDE.md"
    if claude_md.is_file():
        checks.append(CheckResult("D04", "CLAUDE.md", "PASS",
            "Point d'entrée présent"))
    else:
        checks.append(CheckResult("D04", "CLAUDE.md", "WARNING",
            "CLAUDE.md manquant à la racine — Claude Code ne chargera pas le contexte automatiquement"))

    for fname, did in [("TASKS.md", "D05"), ("ISSUES.md", "D06"), ("DECISIONS.md", "D07")]:
        fpath = dcbp_path / fname
        if fpath.is_file():
            checks.append(CheckResult(did, fname, "PASS", "Présent"))
        else:
            checks.append(CheckResult(did, fname, "WARNING",
                f".claude/dcbp/{fname} manquant"))

    # ── CORE SKILLS — WARNING per missing or UNKNOWN collision ─────────────

    skills_dir = project_path / ".claude" / "skills"
    if skills_dir.is_dir():
        checks.append(CheckResult("D08", "Skills dir", "PASS",
            ".claude/skills/ présent"))
    else:
        checks.append(CheckResult("D08", "Skills dir", "WARNING",
            ".claude/skills/ absent — skills non installés. Exécutez: dcbp init"))

    for skill_name, did in sorted(_CORE_SKILL_IDS.items()):
        skill_dir = project_path / ".claude" / "skills" / skill_name
        if not skill_dir.exists():
            checks.append(CheckResult(did, f"Core skill: {skill_name}", "WARNING",
                f"Skill '{skill_name}' absent. Exécutez: dcbp init --force"))
        else:
            ownership = classify_skill(skill_dir)
            if ownership == Ownership.OWNED:
                checks.append(CheckResult(did, f"Core skill: {skill_name}", "PASS",
                    "Présent (OWNED)"))
            else:
                checks.append(CheckResult(did, f"Core skill: {skill_name}", "WARNING",
                    f"Skill '{skill_name}' présent mais appartient à un tiers (UNKNOWN) — préservé par DCBP"))

    # ── LEGACY ─────────────────────────────────────────────────────────────

    legacy_root = project_path / ".dcbp"
    if legacy_root.exists():
        checks.append(CheckResult("D15", "Legacy .dcbp/", "WARNING",
            "Structure .dcbp/ legacy détectée — peut être supprimée manuellement"))
    else:
        checks.append(CheckResult("D15", "Legacy .dcbp/", "PASS",
            "Absent"))

    scripts_dir = dcbp_path / "scripts"
    if scripts_dir.is_dir():
        found = [s for s in LEGACY_SCRIPT_NAMES if (scripts_dir / s).exists()]
        if found:
            checks.append(CheckResult("D16", "Legacy scripts", "WARNING",
                f"Scripts legacy présents: {', '.join(found)} — "
                "ne font plus partie du contract DCBP v1. Suppression manuelle possible."))
        else:
            checks.append(CheckResult("D16", "Legacy scripts", "PASS",
                "Aucun script legacy"))
    else:
        checks.append(CheckResult("D16", "Legacy scripts", "PASS",
            "Aucun script legacy"))

    # ── GLOBAL ~/.claude/skills/ — read-only ───────────────────────────────

    home_skills = Path.home() / ".claude" / "skills"
    if home_skills.is_dir():
        owned_global = []
        for entry in sorted(home_skills.iterdir()):
            if entry.is_dir() and classify_skill(entry) == Ownership.OWNED:
                owned_global.append(entry.name)
        if owned_global:
            checks.append(CheckResult("D17", "Global skills", "WARNING",
                f"Skills DCBP identifiés dans ~/.claude/skills/: {', '.join(owned_global)}. "
                "Exécutez dcbp update pour les retirer proprement."))
        else:
            checks.append(CheckResult("D17", "Global skills", "PASS",
                "Aucun skill DCBP identifié dans ~/.claude/skills/"))
    else:
        checks.append(CheckResult("D17", "Global skills", "PASS",
            "~/.claude/skills/ absent"))

    return DoctorResult(checks=checks)


def print_doctor_result(result: DoctorResult) -> None:
    """Print human-readable doctor output."""
    print("DCBP Doctor")
    print()
    for check in result.checks:
        if check.status == "PASS":
            prefix = "[PASS]"
        elif check.status == "WARNING":
            prefix = "[WARN]"
        else:
            prefix = "[ERRO]"
        print(f"{prefix} {check.id:<3} {check.name:<28} {check.message}")
    print()
    n_pass = len(result.passes)
    n_warn = len(result.warnings)
    n_err = len(result.errors)
    print(f"{n_pass} PASS · {n_warn} WARNING · {n_err} ERROR")
