"""
Tests for DCBP Memory v2 — new install structure, update migration, and contract.

Memory v2 contract:
- New installs: STATE.md present, tasks/ present, PROGRESS.md absent
- Update: conservative migration (PROGRESS.md preserved, STATE.md introduced if absent)
- Doctor: 20-check structure D01-D20
"""

import shutil
from pathlib import Path

import pytest

from dcbp_cli.contract import (
    CORE_SKILL_NAMES,
    MEMORY_V2_ESSENTIAL,
    MEMORY_V2_EXPECTED,
    MEMORY_V2_DIRS,
    LEGACY_FILES,
    LEGACY_SCRIPT_NAMES,
)
from dcbp_cli.commands import init_project, update_templates
from dcbp_cli.doctor import run_checks


# ===========================================================================
# Fixtures
# ===========================================================================

@pytest.fixture
def fake_home(tmp_path, monkeypatch):
    """Fake home directory — never touches real ~/.claude/."""
    home = tmp_path / "fake_home"
    home.mkdir()
    monkeypatch.setattr(Path, "home", staticmethod(lambda: home))
    return home


@pytest.fixture
def fresh_project(tmp_path, fake_home):
    """A freshly initialized Memory v2 project."""
    project = tmp_path / "fresh_project"
    project.mkdir()
    init_project(project, skip_questions=True)
    return project


# ===========================================================================
# Tests: New install — Memory v2 structure
# ===========================================================================

class TestNewInstall:
    def test_state_md_present_after_init(self, fresh_project):
        """New installs must have STATE.md."""
        state = fresh_project / ".claude" / "dcbp" / "STATE.md"
        assert state.is_file(), "STATE.md must be created on init"

    def test_progress_md_absent_after_init(self, fresh_project):
        """New installs must NOT have PROGRESS.md."""
        progress = fresh_project / ".claude" / "dcbp" / "PROGRESS.md"
        assert not progress.exists(), "PROGRESS.md must NOT be created on new installs (Memory v2)"

    def test_tasks_dir_present_after_init(self, fresh_project):
        """New installs must have tasks/ directory."""
        tasks_dir = fresh_project / ".claude" / "dcbp" / "tasks"
        assert tasks_dir.is_dir(), "tasks/ directory must be created on init"

    def test_archive_dir_present_after_init(self, fresh_project):
        """New installs must have archive/ directory."""
        archive_dir = fresh_project / ".claude" / "dcbp" / "archive"
        assert archive_dir.is_dir(), "archive/ directory must be created on init"

    def test_project_md_present_after_init(self, fresh_project):
        """PROJECT.md must be present after init."""
        project_md = fresh_project / ".claude" / "dcbp" / "PROJECT.md"
        assert project_md.is_file()

    def test_tasks_md_present_after_init(self, fresh_project):
        """TASKS.md must be present after init."""
        tasks_md = fresh_project / ".claude" / "dcbp" / "TASKS.md"
        assert tasks_md.is_file()

    def test_state_md_is_readable(self, fresh_project):
        """STATE.md must be a readable file."""
        state = fresh_project / ".claude" / "dcbp" / "STATE.md"
        content = state.read_text(encoding="utf-8")
        assert "Project State" in content

    def test_tasks_md_compact_format(self, fresh_project):
        """TASKS.md must use compact index format (v2)."""
        tasks_md = fresh_project / ".claude" / "dcbp" / "TASKS.md"
        content = tasks_md.read_text(encoding="utf-8")
        # v2 format uses table with ID column
        assert "| ID |" in content

    def test_project_md_v2_sections(self, fresh_project):
        """PROJECT.md must have v2 8-section structure."""
        project_md = fresh_project / ".claude" / "dcbp" / "PROJECT.md"
        content = project_md.read_text(encoding="utf-8")
        # v2 structure has numbered sections
        assert "## 1. Informations" in content
        assert "## 2. Stack" in content
        assert "## 3. Architecture" in content


# ===========================================================================
# Tests: Update — conservative Memory v2 migration
# ===========================================================================

class TestUpdateMigration:
    def test_update_introduces_state_md_if_absent(self, tmp_path, fake_home):
        """update must copy STATE.md from templates if absent (legacy project)."""
        project = tmp_path / "legacy_project"
        project.mkdir()
        # Init (creates STATE.md), then remove it to simulate legacy
        init_project(project, skip_questions=True)
        state = project / ".claude" / "dcbp" / "STATE.md"
        state.unlink()
        assert not state.exists()

        update_templates(project)

        assert state.is_file(), "update must introduce STATE.md if absent"

    def test_update_does_not_overwrite_existing_state_md(self, tmp_path, fake_home):
        """update must NOT overwrite STATE.md if it already exists."""
        project = tmp_path / "existing_project"
        project.mkdir()
        init_project(project, skip_questions=True)
        state = project / ".claude" / "dcbp" / "STATE.md"
        custom_content = "# My custom state\n\nThis is custom.\n"
        state.write_text(custom_content, encoding="utf-8")

        update_templates(project)

        assert state.read_text(encoding="utf-8") == custom_content, (
            "update must not overwrite existing STATE.md"
        )

    def test_update_introduces_tasks_dir_if_absent(self, tmp_path, fake_home):
        """update must create tasks/ if absent."""
        project = tmp_path / "legacy_project2"
        project.mkdir()
        init_project(project, skip_questions=True)
        tasks_dir = project / ".claude" / "dcbp" / "tasks"
        shutil.rmtree(tasks_dir)
        assert not tasks_dir.exists()

        update_templates(project)

        assert tasks_dir.is_dir(), "update must create tasks/ if absent"

    def test_update_never_deletes_progress_md(self, tmp_path, fake_home):
        """update must NEVER delete PROGRESS.md (legacy preservation)."""
        project = tmp_path / "legacy_progress_project"
        project.mkdir()
        init_project(project, skip_questions=True)
        # Manually create PROGRESS.md (simulating a legacy project)
        progress = project / ".claude" / "dcbp" / "PROGRESS.md"
        progress.write_text("# Progress\n\n## [2024-01-01] Old session\n", encoding="utf-8")

        update_templates(project)

        assert progress.is_file(), "update must NEVER delete PROGRESS.md"
        assert "Old session" in progress.read_text(encoding="utf-8"), (
            "update must not modify PROGRESS.md content"
        )

    def test_update_does_not_overwrite_project_md(self, tmp_path, fake_home):
        """update must not overwrite PROJECT.md."""
        project = tmp_path / "project_md_project"
        project.mkdir()
        init_project(project, skip_questions=True)
        project_md = project / ".claude" / "dcbp" / "PROJECT.md"
        custom = "# My Project\n\nCustom content.\n"
        project_md.write_text(custom, encoding="utf-8")

        update_templates(project)

        assert project_md.read_text(encoding="utf-8") == custom

    def test_update_does_not_overwrite_tasks_md(self, tmp_path, fake_home):
        """update must not overwrite TASKS.md."""
        project = tmp_path / "tasks_project"
        project.mkdir()
        init_project(project, skip_questions=True)
        tasks_md = project / ".claude" / "dcbp" / "TASKS.md"
        custom = "# Tasks\n\nMy custom tasks.\n"
        tasks_md.write_text(custom, encoding="utf-8")

        update_templates(project)

        assert tasks_md.read_text(encoding="utf-8") == custom


# ===========================================================================
# Tests: Doctor D01-D20 on new install
# ===========================================================================

class TestDoctorMemoryV2:
    def test_doctor_20_checks_on_new_install(self, fresh_project):
        """Doctor must emit exactly 20 checks on a new install."""
        result = run_checks(fresh_project)
        assert len(result.checks) == 20

    def test_d03_state_md_pass_on_new_install(self, fresh_project):
        """D03 (STATE.md) must PASS on a new install."""
        result = run_checks(fresh_project)
        d03 = next(c for c in result.checks if c.id == "D03")
        assert d03.status == "PASS"

    def test_d08_tasks_dir_pass_on_new_install(self, fresh_project):
        """D08 (tasks/) must PASS on a new install."""
        result = run_checks(fresh_project)
        d08 = next(c for c in result.checks if c.id == "D08")
        assert d08.status == "PASS"

    def test_d19_pass_no_progress_md_on_new_install(self, fresh_project):
        """D19 must PASS (PROGRESS.md absent) on a new install."""
        result = run_checks(fresh_project)
        d19 = next(c for c in result.checks if c.id == "D19")
        assert d19.status == "PASS"

    def test_d03_error_when_state_md_missing(self, fresh_project):
        """D03 must ERROR if STATE.md is missing."""
        state = fresh_project / ".claude" / "dcbp" / "STATE.md"
        state.unlink()
        result = run_checks(fresh_project)
        d03 = next(c for c in result.checks if c.id == "D03")
        assert d03.status == "ERROR"

    def test_d19_warning_when_progress_md_present(self, fresh_project):
        """D19 must WARNING if PROGRESS.md exists (legacy indicator)."""
        progress = fresh_project / ".claude" / "dcbp" / "PROGRESS.md"
        progress.write_text("# Legacy PROGRESS\n", encoding="utf-8")
        result = run_checks(fresh_project)
        d19 = next(c for c in result.checks if c.id == "D19")
        assert d19.status == "WARNING"

    def test_all_check_ids_present(self, fresh_project):
        """All IDs D01-D20 must appear exactly once."""
        result = run_checks(fresh_project)
        ids = [c.id for c in result.checks]
        expected = [f"D{i:02d}" for i in range(1, 21)]
        assert sorted(ids) == sorted(expected)
        assert len(ids) == len(set(ids)), "Duplicate check IDs found"


# ===========================================================================
# Tests: Contract v2 constants
# ===========================================================================

class TestContractV2:
    def test_memory_v2_essential_has_project_and_state(self):
        assert MEMORY_V2_ESSENTIAL == frozenset({"PROJECT.md", "STATE.md"})

    def test_memory_v2_expected_has_three_files(self):
        assert len(MEMORY_V2_EXPECTED) == 3
        assert MEMORY_V2_EXPECTED == frozenset({"TASKS.md", "ISSUES.md", "DECISIONS.md"})

    def test_memory_v2_dirs_has_tasks_and_archive(self):
        assert MEMORY_V2_DIRS == frozenset({"tasks", "archive"})

    def test_legacy_files_has_progress_md(self):
        assert LEGACY_FILES == frozenset({"PROGRESS.md"})

    def test_progress_md_not_in_essential(self):
        assert "PROGRESS.md" not in MEMORY_V2_ESSENTIAL

    def test_progress_md_not_in_expected(self):
        assert "PROGRESS.md" not in MEMORY_V2_EXPECTED
