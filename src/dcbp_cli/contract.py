"""
DCBP Contract v1 — Single source of truth for project structure.
"""
from pathlib import Path

# Core skills installed and managed by DCBP.
# These 6 skills are DCBP-aware (read/write .claude/dcbp/ memory).
CORE_SKILL_NAMES: frozenset = frozenset({
    "archive", "bugfix", "dev", "etat", "review", "start",
})

# Legacy scripts distributed before v0.7.0.
# No longer part of the contract — only referenced for legacy detection.
LEGACY_SCRIPT_NAMES: tuple = (
    "init_task.py",
    "update_progress.py",
    "sync_memory.py",
)
