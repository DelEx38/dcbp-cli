"""
Tests for DCBP Doctor and Contract modules.

Doctor contract: strictly read-only — never creates, modifies, or deletes any file.
"""

import shutil
from pathlib import Path

import pytest

from dcbp_cli.contract import CORE_SKILL_NAMES, LEGACY_SCRIPT_NAMES
from dcbp_cli.doctor import (
    CheckResult,
    DoctorResult,
    run_checks,
    print_doctor_result,
)
from dcbp_cli.commands import init_project


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
def initialized_project(tmp_path, fake_home):
    """A project that has been fully initialized with dcbp init."""
    project = tmp_path / "test_project"
    project.mkdir()
    init_project(project, skip_questions=True)
    return project


@pytest.fixture
def empty_project(tmp_path, fake_home):
    """An empty project directory (no DCBP)."""
    project = tmp_path / "empty_project"
    project.mkdir()
    return project


# ===========================================================================
# Tests: Contract constants
# ===========================================================================

class TestContract:
    def test_core_skill_names_is_frozenset(self):
        assert isinstance(CORE_SKILL_NAMES, frozenset)

    def test_core_skill_names_has_6_entries(self):
        assert len(CORE_SKILL_NAMES) == 6

    def test_core_skill_names_content(self):
        assert CORE_SKILL_NAMES == frozenset({
            "archive", "bugfix", "dev", "etat", "review", "start"
        })

    def test_legacy_script_names_is_tuple(self):
        assert isinstance(LEGACY_SCRIPT_NAMES, tuple)

    def test_legacy_script_names_content(self):
        assert "init_task.py" in LEGACY_SCRIPT_NAMES
        assert "update_progress.py" in LEGACY_SCRIPT_NAMES
        assert "sync_memory.py" in LEGACY_SCRIPT_NAMES


# ===========================================================================
# Tests: DoctorResult dataclass
# ===========================================================================

class TestDoctorResult:
    def test_empty_result_has_zero_exit_code(self):
        result = DoctorResult()
        assert result.exit_code == 0

    def test_errors_returns_only_errors(self):
        result = DoctorResult(checks=[
            CheckResult("D01", "test", "ERROR", "err"),
            CheckResult("D02", "test2", "PASS", "ok"),
            CheckResult("D03", "test3", "WARNING", "warn"),
        ])
        assert len(result.errors) == 1
        assert result.errors[0].id == "D01"

    def test_warnings_returns_only_warnings(self):
        result = DoctorResult(checks=[
            CheckResult("D01", "test", "ERROR", "err"),
            CheckResult("D02", "test2", "PASS", "ok"),
            CheckResult("D03", "test3", "WARNING", "warn"),
        ])
        assert len(result.warnings) == 1
        assert result.warnings[0].id == "D03"

    def test_passes_returns_only_passes(self):
        result = DoctorResult(checks=[
            CheckResult("D01", "test", "ERROR", "err"),
            CheckResult("D02", "test2", "PASS", "ok"),
            CheckResult("D03", "test3", "WARNING", "warn"),
        ])
        assert len(result.passes) == 1
        assert result.passes[0].id == "D02"

    def test_exit_code_2_when_errors(self):
        result = DoctorResult(checks=[
            CheckResult("D01", "test", "ERROR", "err"),
        ])
        assert result.exit_code == 2

    def test_exit_code_1_when_warnings_only(self):
        result = DoctorResult(checks=[
            CheckResult("D01", "test", "WARNING", "warn"),
        ])
        assert result.exit_code == 1

    def test_exit_code_0_when_all_pass(self):
        result = DoctorResult(checks=[
            CheckResult("D01", "test", "PASS", "ok"),
        ])
        assert result.exit_code == 0

    def test_exit_code_2_beats_warning(self):
        """Errors take precedence: exit_code=2 even if there are also warnings."""
        result = DoctorResult(checks=[
            CheckResult("D01", "test", "ERROR", "err"),
            CheckResult("D02", "test2", "WARNING", "warn"),
        ])
        assert result.exit_code == 2


# ===========================================================================
# Tests: run_checks — uninitialized project
# ===========================================================================

class TestRunChecksUninitialized:
    def test_empty_project_has_errors(self, empty_project):
        result = run_checks(empty_project)
        assert result.exit_code == 2

    def test_d01_error_when_no_dcbp_dir(self, empty_project):
        result = run_checks(empty_project)
        d01 = next(c for c in result.checks if c.id == "D01")
        assert d01.status == "ERROR"

    def test_d02_error_when_no_project_md(self, empty_project):
        result = run_checks(empty_project)
        d02 = next(c for c in result.checks if c.id == "D02")
        assert d02.status == "ERROR"

    def test_d03_error_when_no_progress_md(self, empty_project):
        result = run_checks(empty_project)
        d03 = next(c for c in result.checks if c.id == "D03")
        assert d03.status == "ERROR"

    def test_d04_warning_when_no_claude_md(self, empty_project):
        result = run_checks(empty_project)
        d04 = next(c for c in result.checks if c.id == "D04")
        assert d04.status == "WARNING"

    def test_total_check_count(self, empty_project):
        """Doctor always emits exactly 17 checks."""
        result = run_checks(empty_project)
        assert len(result.checks) == 17

    def test_check_ids_are_d01_to_d17(self, empty_project):
        result = run_checks(empty_project)
        ids = {c.id for c in result.checks}
        expected = {f"D{i:02d}" for i in range(1, 18)}
        assert ids == expected


# ===========================================================================
# Tests: run_checks — initialized project
# ===========================================================================

class TestRunChecksInitialized:
    def test_d01_pass_after_init(self, initialized_project):
        result = run_checks(initialized_project)
        d01 = next(c for c in result.checks if c.id == "D01")
        assert d01.status == "PASS"

    def test_d02_pass_after_init(self, initialized_project):
        result = run_checks(initialized_project)
        d02 = next(c for c in result.checks if c.id == "D02")
        assert d02.status == "PASS"

    def test_d03_pass_after_init(self, initialized_project):
        result = run_checks(initialized_project)
        d03 = next(c for c in result.checks if c.id == "D03")
        assert d03.status == "PASS"

    def test_d04_pass_after_init(self, initialized_project):
        """CLAUDE.md should be present after init."""
        result = run_checks(initialized_project)
        d04 = next(c for c in result.checks if c.id == "D04")
        assert d04.status == "PASS"

    def test_d08_pass_after_init(self, initialized_project):
        result = run_checks(initialized_project)
        d08 = next(c for c in result.checks if c.id == "D08")
        assert d08.status == "PASS"

    def test_core_skills_pass_after_init(self, initialized_project):
        """All 6 core skills should be PASS after init."""
        result = run_checks(initialized_project)
        core_check_ids = {"D09", "D10", "D11", "D12", "D13", "D14"}
        for check in result.checks:
            if check.id in core_check_ids:
                assert check.status == "PASS", (
                    f"Check {check.id} ({check.name}) should PASS but got {check.status}: {check.message}"
                )

    def test_d15_pass_no_legacy_dcbp_dir(self, initialized_project):
        result = run_checks(initialized_project)
        d15 = next(c for c in result.checks if c.id == "D15")
        assert d15.status == "PASS"

    def test_d16_pass_no_legacy_scripts(self, initialized_project):
        result = run_checks(initialized_project)
        d16 = next(c for c in result.checks if c.id == "D16")
        assert d16.status == "PASS"

    def test_d17_pass_no_global_skills(self, initialized_project, fake_home):
        result = run_checks(initialized_project)
        d17 = next(c for c in result.checks if c.id == "D17")
        assert d17.status == "PASS"


# ===========================================================================
# Tests: run_checks — legacy detection
# ===========================================================================

class TestRunChecksLegacy:
    def test_d15_warning_when_legacy_dcbp_dir_exists(self, initialized_project):
        legacy = initialized_project / ".dcbp"
        legacy.mkdir()
        result = run_checks(initialized_project)
        d15 = next(c for c in result.checks if c.id == "D15")
        assert d15.status == "WARNING"

    def test_d16_warning_when_legacy_scripts_present(self, initialized_project):
        scripts_dir = initialized_project / ".claude" / "dcbp" / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        (scripts_dir / "init_task.py").write_text("# legacy script", encoding="utf-8")
        result = run_checks(initialized_project)
        d16 = next(c for c in result.checks if c.id == "D16")
        assert d16.status == "WARNING"
        assert "init_task.py" in d16.message

    def test_d16_pass_when_scripts_dir_exists_but_no_legacy_files(self, initialized_project):
        scripts_dir = initialized_project / ".claude" / "dcbp" / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        (scripts_dir / "some_other_script.py").write_text("# not legacy", encoding="utf-8")
        result = run_checks(initialized_project)
        d16 = next(c for c in result.checks if c.id == "D16")
        assert d16.status == "PASS"

    def test_d17_warning_when_global_owned_skills_present(self, initialized_project, fake_home):
        global_skills = fake_home / ".claude" / "skills"
        global_skills.mkdir(parents=True)
        owned_dir = global_skills / "start"
        owned_dir.mkdir()
        (owned_dir / "SKILL.md").write_text(
            "---\nname: start\ntool: dcbp\n---\n# Start\n",
            encoding="utf-8"
        )
        result = run_checks(initialized_project)
        d17 = next(c for c in result.checks if c.id == "D17")
        assert d17.status == "WARNING"
        assert "start" in d17.message

    def test_d17_pass_when_global_skills_has_only_unknown(self, initialized_project, fake_home):
        global_skills = fake_home / ".claude" / "skills"
        global_skills.mkdir(parents=True)
        unknown_dir = global_skills / "my_custom"
        unknown_dir.mkdir()
        (unknown_dir / "SKILL.md").write_text(
            "---\nname: my_custom\n---\n# Custom\n",
            encoding="utf-8"
        )
        result = run_checks(initialized_project)
        d17 = next(c for c in result.checks if c.id == "D17")
        assert d17.status == "PASS"


# ===========================================================================
# Tests: run_checks — missing optional memory files
# ===========================================================================

class TestRunChecksMissingOptional:
    def test_d05_warning_when_tasks_md_missing(self, initialized_project):
        tasks = initialized_project / ".claude" / "dcbp" / "TASKS.md"
        tasks.unlink()
        result = run_checks(initialized_project)
        d05 = next(c for c in result.checks if c.id == "D05")
        assert d05.status == "WARNING"

    def test_d06_warning_when_issues_md_missing(self, initialized_project):
        issues = initialized_project / ".claude" / "dcbp" / "ISSUES.md"
        issues.unlink()
        result = run_checks(initialized_project)
        d06 = next(c for c in result.checks if c.id == "D06")
        assert d06.status == "WARNING"

    def test_d07_warning_when_decisions_md_missing(self, initialized_project):
        decisions = initialized_project / ".claude" / "dcbp" / "DECISIONS.md"
        decisions.unlink()
        result = run_checks(initialized_project)
        d07 = next(c for c in result.checks if c.id == "D07")
        assert d07.status == "WARNING"


# ===========================================================================
# Tests: run_checks — missing core skills
# ===========================================================================

class TestRunChecksMissingCoreSkills:
    def test_missing_core_skill_is_warning(self, initialized_project):
        dev_skill = initialized_project / ".claude" / "skills" / "dev"
        shutil.rmtree(dev_skill)
        result = run_checks(initialized_project)
        d11 = next(c for c in result.checks if c.id == "D11")
        assert d11.status == "WARNING"
        assert "dev" in d11.message

    def test_third_party_core_skill_is_warning(self, initialized_project):
        """A core skill dir owned by third party should be WARNING, not ERROR."""
        dev_skill = initialized_project / ".claude" / "skills" / "dev"
        skill_md = dev_skill / "SKILL.md"
        # Overwrite with third-party content
        skill_md.write_text(
            "---\nname: dev\ndescription: third-party\n---\n# Generic dev\n",
            encoding="utf-8"
        )
        result = run_checks(initialized_project)
        d11 = next(c for c in result.checks if c.id == "D11")
        assert d11.status == "WARNING"
        assert "UNKNOWN" in d11.message

    def test_d08_warning_when_skills_dir_absent(self, initialized_project):
        skills_dir = initialized_project / ".claude" / "skills"
        shutil.rmtree(skills_dir)
        result = run_checks(initialized_project)
        d08 = next(c for c in result.checks if c.id == "D08")
        assert d08.status == "WARNING"


# ===========================================================================
# Tests: Doctor is strictly read-only
# ===========================================================================

class TestDoctorReadOnly:
    def _snapshot_dir(self, path: Path) -> dict:
        """Return a dict of {relative_path: mtime_ns} for all files under path."""
        snapshot = {}
        if path.exists():
            for f in path.rglob("*"):
                if f.is_file():
                    rel = f.relative_to(path)
                    snapshot[str(rel)] = f.stat().st_mtime_ns
        return snapshot

    def test_doctor_does_not_modify_any_file(self, initialized_project, fake_home):
        """Doctor must not modify any existing file."""
        snapshot_before = self._snapshot_dir(initialized_project)

        run_checks(initialized_project)

        snapshot_after = self._snapshot_dir(initialized_project)
        for path, mtime in snapshot_before.items():
            assert path in snapshot_after, f"File disappeared: {path}"
            assert snapshot_after[path] == mtime, f"File was modified: {path}"

    def test_doctor_does_not_create_files(self, empty_project, fake_home):
        """Doctor must not create any file in an empty project."""
        files_before = set(empty_project.rglob("*"))

        run_checks(empty_project)

        files_after = set(empty_project.rglob("*"))
        new_files = files_after - files_before
        assert not new_files, f"Doctor created files: {new_files}"

    def test_doctor_does_not_delete_files(self, initialized_project, fake_home):
        """Doctor must not delete any file."""
        files_before = set(initialized_project.rglob("*"))

        run_checks(initialized_project)

        files_after = set(initialized_project.rglob("*"))
        deleted_files = files_before - files_after
        assert not deleted_files, f"Doctor deleted files: {deleted_files}"

    def test_doctor_does_not_touch_home(self, initialized_project, fake_home):
        """Doctor must not modify the home directory."""
        snapshot_before = self._snapshot_dir(fake_home)

        run_checks(initialized_project)

        snapshot_after = self._snapshot_dir(fake_home)
        assert snapshot_before == snapshot_after, "Doctor modified home directory"


# ===========================================================================
# Tests: print_doctor_result
# ===========================================================================

class TestPrintDoctorResult:
    def test_prints_header(self, capsys):
        result = DoctorResult(checks=[])
        print_doctor_result(result)
        captured = capsys.readouterr()
        assert "DCBP Doctor" in captured.out

    def test_prints_pass_prefix(self, capsys):
        result = DoctorResult(checks=[
            CheckResult("D01", "Test check", "PASS", "All good")
        ])
        print_doctor_result(result)
        captured = capsys.readouterr()
        assert "[PASS]" in captured.out

    def test_prints_warn_prefix(self, capsys):
        result = DoctorResult(checks=[
            CheckResult("D01", "Test check", "WARNING", "Something missing")
        ])
        print_doctor_result(result)
        captured = capsys.readouterr()
        assert "[WARN]" in captured.out

    def test_prints_erro_prefix(self, capsys):
        result = DoctorResult(checks=[
            CheckResult("D01", "Test check", "ERROR", "Critical issue")
        ])
        print_doctor_result(result)
        captured = capsys.readouterr()
        assert "[ERRO]" in captured.out

    def test_prints_summary_counts(self, capsys):
        result = DoctorResult(checks=[
            CheckResult("D01", "a", "PASS", "ok"),
            CheckResult("D02", "b", "WARNING", "warn"),
            CheckResult("D03", "c", "ERROR", "err"),
        ])
        print_doctor_result(result)
        captured = capsys.readouterr()
        assert "1 PASS" in captured.out
        assert "1 WARNING" in captured.out
        assert "1 ERROR" in captured.out
