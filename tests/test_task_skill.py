"""
Tests for /task skill contract, Memory v2 integration, and Doctor D17/D22/D23.
"""
import json
import pytest
from pathlib import Path
from dcbp_cli.contract import (
    CORE_SKILL_NAMES,
    GUARDRAIL_SCRIPT,
    PUSH_AUTH_FILE,
    SETTINGS_FILE,
)
from dcbp_cli.doctor import run_checks
from dcbp_cli.commands import init_project, classify_skill, Ownership


# ===========================================================================
# Helpers
# ===========================================================================

def _templates_path() -> Path:
    from dcbp_cli.commands import get_templates_path
    return get_templates_path()


# ===========================================================================
# Tests: /task in core catalog
# ===========================================================================

class TestTaskInCatalog:
    def test_task_in_core_skill_names(self):
        assert "task" in CORE_SKILL_NAMES

    def test_core_skill_names_has_7_skills(self):
        assert len(CORE_SKILL_NAMES) == 7

    def test_task_skill_template_exists(self):
        task_skill = _templates_path() / ".claude" / "skills" / "task" / "SKILL.md"
        assert task_skill.is_file(), "task/SKILL.md must exist in templates"

    def test_task_skill_has_dcbp_frontmatter(self):
        task_skill = _templates_path() / ".claude" / "skills" / "task" / "SKILL.md"
        content = task_skill.read_text(encoding="utf-8")
        assert "tool: dcbp" in content
        assert "name: task" in content

    def test_task_skill_classified_owned(self):
        task_dir = _templates_path() / ".claude" / "skills" / "task"
        assert classify_skill(task_dir) == Ownership.OWNED


# ===========================================================================
# Tests: task skill installed on fresh init
# ===========================================================================

class TestTaskSkillInstalled:
    def test_task_skill_present_after_init(self, tmp_path):
        init_project(tmp_path, skip_questions=True)
        task_dir = tmp_path / ".claude" / "skills" / "task"
        assert task_dir.is_dir()
        assert (task_dir / "SKILL.md").is_file()

    def test_d17_pass_task_skill_after_init(self, tmp_path):
        """D17 (Core skill: task) must PASS after init."""
        init_project(tmp_path, skip_questions=True)
        result = run_checks(tmp_path)
        d17 = next(c for c in result.checks if c.id == "D17")
        assert d17.status == "PASS", f"D17 expected PASS, got {d17.status}: {d17.message}"

    def test_task_skill_ownership_after_init(self, tmp_path):
        init_project(tmp_path, skip_questions=True)
        task_dir = tmp_path / ".claude" / "skills" / "task"
        assert classify_skill(task_dir) == Ownership.OWNED


# ===========================================================================
# Tests: guardrail installation
# ===========================================================================

class TestGuardrailInstalled:
    def test_guardrail_script_template_exists(self):
        guard = _templates_path() / ".claude" / "dcbp" / "guardrail" / "push_guard.py"
        assert guard.is_file(), "push_guard.py must exist in templates"

    def test_guardrail_installed_after_init(self, tmp_path):
        init_project(tmp_path, skip_questions=True)
        guard = tmp_path / ".claude" / "dcbp" / "guardrail" / "push_guard.py"
        assert guard.is_file(), "push_guard.py must be installed by dcbp init"

    def test_d22_pass_after_init(self, tmp_path):
        """D22 (Guardrail script) must PASS after init."""
        init_project(tmp_path, skip_questions=True)
        result = run_checks(tmp_path)
        d22 = next(c for c in result.checks if c.id == "D22")
        assert d22.status == "PASS", f"D22 expected PASS, got {d22.status}: {d22.message}"

    def test_d22_warning_when_guardrail_missing(self, tmp_path):
        """D22 must WARNING if guardrail script is absent."""
        init_project(tmp_path, skip_questions=True)
        guard = tmp_path / ".claude" / "dcbp" / "guardrail" / "push_guard.py"
        guard.unlink()
        result = run_checks(tmp_path)
        d22 = next(c for c in result.checks if c.id == "D22")
        assert d22.status == "WARNING"


# ===========================================================================
# Tests: settings.json hook installation
# ===========================================================================

class TestSettingsJsonInstalled:
    def test_settings_template_exists(self):
        settings = _templates_path() / ".claude" / "settings.json"
        assert settings.is_file(), "settings.json must exist in templates"

    def test_settings_template_has_hook(self):
        settings = _templates_path() / ".claude" / "settings.json"
        data = json.loads(settings.read_text(encoding="utf-8"))
        hooks = data.get("hooks", {})
        pre = hooks.get("PreToolUse", [])
        assert len(pre) > 0, "settings.json must have PreToolUse hooks"
        hook_commands = [
            h.get("command", "")
            for entry in pre
            for h in entry.get("hooks", [])
        ]
        assert any("push_guard" in cmd for cmd in hook_commands)

    def test_settings_json_installed_after_init(self, tmp_path):
        init_project(tmp_path, skip_questions=True)
        settings = tmp_path / ".claude" / "settings.json"
        assert settings.is_file(), ".claude/settings.json must be installed by dcbp init"

    def test_d23_pass_after_init(self, tmp_path):
        """D23 (Push hook config) must PASS after init."""
        init_project(tmp_path, skip_questions=True)
        result = run_checks(tmp_path)
        d23 = next(c for c in result.checks if c.id == "D23")
        assert d23.status == "PASS", f"D23 expected PASS, got {d23.status}: {d23.message}"

    def test_d23_warning_when_settings_missing(self, tmp_path):
        """D23 must WARNING if settings.json is absent."""
        init_project(tmp_path, skip_questions=True)
        (tmp_path / ".claude" / "settings.json").unlink()
        result = run_checks(tmp_path)
        d23 = next(c for c in result.checks if c.id == "D23")
        assert d23.status == "WARNING"

    def test_d23_warning_when_hook_absent_from_settings(self, tmp_path):
        """D23 must WARNING if settings.json exists but has no push_guard hook."""
        init_project(tmp_path, skip_questions=True)
        settings = tmp_path / ".claude" / "settings.json"
        settings.write_text('{"theme": "dark"}', encoding="utf-8")
        result = run_checks(tmp_path)
        d23 = next(c for c in result.checks if c.id == "D23")
        assert d23.status == "WARNING"

    def test_settings_not_overwritten_if_exists(self, tmp_path):
        """settings.json must not be overwritten if already present."""
        custom = tmp_path / ".claude"
        custom.mkdir(parents=True, exist_ok=True)
        settings = custom / "settings.json"
        settings.write_text('{"custom": true}', encoding="utf-8")

        init_project(tmp_path, skip_questions=True)

        content = json.loads(settings.read_text(encoding="utf-8"))
        assert content.get("custom") is True, "Existing settings.json must not be overwritten"


# ===========================================================================
# Tests: contract constants
# ===========================================================================

class TestContractConstants:
    def test_push_auth_file_constant(self):
        assert PUSH_AUTH_FILE == ".push_auth"

    def test_guardrail_script_constant(self):
        assert "push_guard.py" in GUARDRAIL_SCRIPT

    def test_settings_file_constant(self):
        assert "settings.json" in SETTINGS_FILE

    def test_push_auth_not_in_memory_files(self):
        from dcbp_cli.contract import MEMORY_V2_ESSENTIAL, MEMORY_V2_EXPECTED
        assert PUSH_AUTH_FILE not in MEMORY_V2_ESSENTIAL
        assert PUSH_AUTH_FILE not in MEMORY_V2_EXPECTED


# ===========================================================================
# Tests: Doctor D01-D23 on new install (full smoke)
# ===========================================================================

class TestDoctorFullNewInstall:
    def test_23_checks_after_init(self, tmp_path):
        init_project(tmp_path, skip_questions=True)
        result = run_checks(tmp_path)
        assert len(result.checks) == 23

    def test_all_pass_after_init(self, tmp_path):
        """After a clean init, all 23 checks must PASS (no warnings, no errors)."""
        init_project(tmp_path, skip_questions=True)
        result = run_checks(tmp_path)
        failures = [
            f"{c.id} {c.status}: {c.message}"
            for c in result.checks
            if c.status != "PASS"
        ]
        assert not failures, f"Expected all PASS but got:\n" + "\n".join(failures)
