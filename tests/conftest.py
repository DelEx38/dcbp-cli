"""
Pytest configuration and shared fixtures for DCBP CLI tests.
All filesystem tests use tmp_path and monkeypatched Path.home().
NEVER touches real ~/.claude/skills/.
"""

import shutil
from pathlib import Path
import pytest


# ---------------------------------------------------------------------------
# Core fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def fake_home(tmp_path, monkeypatch):
    """
    Provide a fake home directory and monkeypatch Path.home() to return it.
    Any test using this fixture will NEVER touch the real ~/.claude/.
    """
    home = tmp_path / "fake_home"
    home.mkdir()
    monkeypatch.setattr(Path, "home", staticmethod(lambda: home))
    return home


@pytest.fixture
def fake_project(tmp_path):
    """Provide a clean temporary project directory."""
    project = tmp_path / "test_project"
    project.mkdir()
    return project


@pytest.fixture
def templates_path():
    """Return the path to the DCBP CLI templates directory."""
    from dcbp_cli.commands import get_templates_path
    return get_templates_path()


@pytest.fixture
def third_party_skill_content():
    """
    Valid SKILL.md content for a third-party skill.
    Contains no DCBP markers and no tool: dcbp frontmatter.
    """
    return """\
---
name: dev
description: "My custom dev workflow"
allowed-tools: Read, Edit, Write
---

# My Custom Dev Skill

This is a third-party skill that DCBP must never overwrite.
It does not reference .claude/dcbp/ or any DCBP marker.
"""


@pytest.fixture
def dcbp_owned_skill_content():
    """
    Valid SKILL.md content for a DCBP-owned skill (has tool: dcbp frontmatter).
    """
    return """\
---
name: dev
description: "DCBP dev skill"
tool: dcbp
allowed-tools: Read, Edit, Write, Bash
---

# /dev - Développement Structuré

References .claude/dcbp/ for memory.
"""
