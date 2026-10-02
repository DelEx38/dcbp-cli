"""
DCBP Contract v2 — Single source of truth for Memory v2 project structure.
Extended for v0.9.0 Workflow Engine.
"""
from pathlib import Path

# ── Core skills ────────────────────────────────────────────────────────────────

# Active core skill catalog (v0.9.0)
CORE_SKILL_NAMES: frozenset = frozenset({
    "archive", "bugfix", "dev", "etat", "review", "start", "task",
})

# ── Memory v2 ──────────────────────────────────────────────────────────────────

# Essential files (absence → ERROR in Doctor)
MEMORY_V2_ESSENTIAL: frozenset = frozenset({
    "PROJECT.md",
    "STATE.md",
})

# Expected files (absence → WARNING in Doctor)
MEMORY_V2_EXPECTED: frozenset = frozenset({
    "TASKS.md",
    "ISSUES.md",
    "DECISIONS.md",
})

# Expected directories (absence → WARNING)
MEMORY_V2_DIRS: frozenset = frozenset({
    "tasks",
    "archive",
})

# Legacy files — present in older projects, must never be deleted
LEGACY_FILES: frozenset = frozenset({
    "PROGRESS.md",
})

# Legacy scripts distributed before v0.7.0
LEGACY_SCRIPT_NAMES: tuple = (
    "init_task.py",
    "update_progress.py",
    "sync_memory.py",
)

# ── Workflow Engine (v0.9.0) ───────────────────────────────────────────────────

# Push authorization file — local, non-tracked, one-time use
PUSH_AUTH_FILE: str = ".push_auth"   # relative to .claude/dcbp/

# Guardrail script — installed by dcbp init/update
GUARDRAIL_SCRIPT: str = "guardrail/push_guard.py"   # relative to .claude/dcbp/

# Claude Code project settings file — installs the PreToolUse hook
SETTINGS_FILE: str = ".claude/settings.json"  # relative to project root
