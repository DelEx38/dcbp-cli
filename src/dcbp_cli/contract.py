"""
DCBP Contract v2 — Single source of truth for Memory v2 project structure.
"""
from pathlib import Path

# Core skills installed and managed by DCBP (Contract v1, unchanged).
CORE_SKILL_NAMES: frozenset = frozenset({
    "archive", "bugfix", "dev", "etat", "review", "start",
})

# Memory v2 — essential files (absence → ERROR in Doctor)
MEMORY_V2_ESSENTIAL: frozenset = frozenset({
    "PROJECT.md",
    "STATE.md",
})

# Memory v2 — expected files (absence → WARNING in Doctor)
MEMORY_V2_EXPECTED: frozenset = frozenset({
    "TASKS.md",
    "ISSUES.md",
    "DECISIONS.md",
})

# Memory v2 — expected directories (absence → WARNING)
MEMORY_V2_DIRS: frozenset = frozenset({
    "tasks",
    "archive",
})

# Legacy files — present in older projects, must never be deleted
LEGACY_FILES: frozenset = frozenset({
    "PROGRESS.md",
})

# Legacy scripts distributed before v0.7.0.
# No longer part of the contract — only referenced for legacy detection.
LEGACY_SCRIPT_NAMES: tuple = (
    "init_task.py",
    "update_progress.py",
    "sync_memory.py",
)
