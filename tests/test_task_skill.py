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
from dcbp_cli.commands import (
    init_project,
    classify_skill,
    Ownership,
    update_templates,
    _merge_dcbp_hook_into_settings,
)


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


# ===========================================================================
# Tests: settings.json conservative merge (Fix-01)
# ===========================================================================

class TestSettingsMigration:
    """Tests for _merge_dcbp_hook_into_settings and update_templates behavior."""

    def _dcbp_path(self, tmp_path: Path) -> Path:
        return tmp_path / ".claude" / "dcbp"

    # ── _merge_dcbp_hook_into_settings ──────────────────────────────────────

    def test_merge_adds_hook_when_no_hooks_key(self, tmp_path):
        """settings.json with no 'hooks' key → hook added."""
        settings = tmp_path / "settings.json"
        settings.write_text('{"theme": "dark"}', encoding="utf-8")

        result = _merge_dcbp_hook_into_settings(settings)
        assert result == "added"

        data = json.loads(settings.read_text(encoding="utf-8"))
        cmds = [
            h.get("command", "")
            for entry in data["hooks"]["PreToolUse"]
            for h in entry.get("hooks", [])
        ]
        assert any("push_guard" in c for c in cmds)

    def test_merge_adds_hook_to_empty_pre_tool_use(self, tmp_path):
        """settings.json with empty PreToolUse list → hook added."""
        settings = tmp_path / "settings.json"
        settings.write_text('{"hooks": {"PreToolUse": []}}', encoding="utf-8")

        result = _merge_dcbp_hook_into_settings(settings)
        assert result == "added"

        data = json.loads(settings.read_text(encoding="utf-8"))
        assert len(data["hooks"]["PreToolUse"]) == 1

    def test_merge_detects_already_present(self, tmp_path):
        """Hook already present → returns 'already_present', no duplicate added."""
        existing = {
            "hooks": {
                "PreToolUse": [
                    {
                        "matcher": "Bash",
                        "hooks": [
                            {"type": "command", "command": "python .claude/dcbp/guardrail/push_guard.py"}
                        ],
                    }
                ]
            }
        }
        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps(existing), encoding="utf-8")

        result = _merge_dcbp_hook_into_settings(settings)
        assert result == "already_present"

        data = json.loads(settings.read_text(encoding="utf-8"))
        assert len(data["hooks"]["PreToolUse"]) == 1, "No duplicate must be added"

    def test_merge_idempotent_double_call(self, tmp_path):
        """Calling merge twice results in exactly one DCBP hook."""
        settings = tmp_path / "settings.json"
        settings.write_text('{"hooks": {"PreToolUse": []}}', encoding="utf-8")

        _merge_dcbp_hook_into_settings(settings)
        result2 = _merge_dcbp_hook_into_settings(settings)
        assert result2 == "already_present"

        data = json.loads(settings.read_text(encoding="utf-8"))
        assert len(data["hooks"]["PreToolUse"]) == 1

    def test_merge_preserves_existing_hooks(self, tmp_path):
        """Other hooks are preserved unchanged when DCBP hook is added."""
        existing = {
            "hooks": {
                "PreToolUse": [
                    {
                        "matcher": "Edit",
                        "hooks": [{"type": "command", "command": "echo hello"}],
                    }
                ]
            }
        }
        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps(existing), encoding="utf-8")

        _merge_dcbp_hook_into_settings(settings)

        data = json.loads(settings.read_text(encoding="utf-8"))
        entries = data["hooks"]["PreToolUse"]
        assert len(entries) == 2
        matchers = [e.get("matcher") for e in entries]
        assert "Edit" in matchers

    def test_merge_preserves_malformed_json(self, tmp_path):
        """Malformed JSON is never overwritten — preserves the file."""
        bad_content = "{ not valid json !!!"
        settings = tmp_path / "settings.json"
        settings.write_text(bad_content, encoding="utf-8")

        result = _merge_dcbp_hook_into_settings(settings)
        assert result == "preserved_malformed"
        assert settings.read_text(encoding="utf-8") == bad_content

    def test_merge_preserves_non_dict_json(self, tmp_path):
        """JSON that is not an object (e.g., array) is preserved unchanged."""
        settings = tmp_path / "settings.json"
        settings.write_text('["array", "not", "object"]', encoding="utf-8")

        result = _merge_dcbp_hook_into_settings(settings)
        assert result == "preserved_malformed"

    # ── update_templates behavior ────────────────────────────────────────────

    def test_update_merges_hook_into_existing_settings(self, tmp_path):
        """dcbp update must add DCBP hook into existing settings.json."""
        # First install without settings (simulate old install)
        init_project(tmp_path, skip_questions=True)
        settings = tmp_path / ".claude" / "settings.json"

        # Overwrite with custom settings (no hook)
        settings.write_text('{"theme": "dark"}', encoding="utf-8")

        # Now run update
        update_templates(tmp_path)

        data = json.loads(settings.read_text(encoding="utf-8"))
        # Theme preserved
        assert data.get("theme") == "dark"
        # Hook added
        cmds = [
            h.get("command", "")
            for entry in data.get("hooks", {}).get("PreToolUse", [])
            for h in entry.get("hooks", [])
        ]
        assert any("push_guard" in c for c in cmds)

    def test_update_does_not_duplicate_existing_hook(self, tmp_path):
        """Running update twice must not duplicate the DCBP hook."""
        init_project(tmp_path, skip_questions=True)

        update_templates(tmp_path)

        settings = tmp_path / ".claude" / "settings.json"
        data = json.loads(settings.read_text(encoding="utf-8"))
        all_cmds = [
            h.get("command", "")
            for entry in data.get("hooks", {}).get("PreToolUse", [])
            for h in entry.get("hooks", [])
        ]
        push_guard_count = sum(1 for c in all_cmds if "push_guard" in c)
        assert push_guard_count == 1, f"Expected exactly 1 push_guard hook, found {push_guard_count}"

    def test_update_preserves_custom_settings_when_adding_hook(self, tmp_path):
        """Custom settings keys must survive update merge."""
        init_project(tmp_path, skip_questions=True)
        settings = tmp_path / ".claude" / "settings.json"
        # Add custom key
        data = json.loads(settings.read_text(encoding="utf-8"))
        data["custom_key"] = "preserved"
        settings.write_text(json.dumps(data), encoding="utf-8")

        update_templates(tmp_path)

        result = json.loads(settings.read_text(encoding="utf-8"))
        assert result.get("custom_key") == "preserved"

    def test_update_preserves_malformed_settings(self, tmp_path):
        """Malformed settings.json must not be overwritten by update."""
        init_project(tmp_path, skip_questions=True)
        settings = tmp_path / ".claude" / "settings.json"
        bad = "{ broken json"
        settings.write_text(bad, encoding="utf-8")

        update_templates(tmp_path)

        assert settings.read_text(encoding="utf-8") == bad
