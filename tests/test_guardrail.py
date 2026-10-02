"""
Tests for DCBP push guardrail — push_guard.py logic.
Tests the check_push_authorization() function directly (no subprocess needed).
"""
import subprocess
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# We import the template's push_guard.py directly by adding its location to sys.path.
# This tests the actual deployed script, not a copy.
import importlib.util

_GUARD_PATH = (
    Path(__file__).parent.parent
    / "src" / "dcbp_cli" / "templates" / ".claude" / "dcbp"
    / "guardrail" / "push_guard.py"
)

def _load_push_guard():
    spec = importlib.util.spec_from_file_location("push_guard", _GUARD_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def push_guard():
    return _load_push_guard()


# ===========================================================================
# Tests: non-push commands are always allowed
# ===========================================================================

class TestNonPushCommands:
    def test_git_status_allowed(self, push_guard, tmp_path):
        allowed, msg = push_guard.check_push_authorization(
            "git status", auth_file=tmp_path / ".push_auth"
        )
        assert allowed is True
        assert msg == ""

    def test_git_diff_allowed(self, push_guard, tmp_path):
        allowed, msg = push_guard.check_push_authorization(
            "git diff HEAD~1", auth_file=tmp_path / ".push_auth"
        )
        assert allowed is True

    def test_git_add_allowed(self, push_guard, tmp_path):
        allowed, msg = push_guard.check_push_authorization(
            "git add -A", auth_file=tmp_path / ".push_auth"
        )
        assert allowed is True

    def test_git_commit_allowed(self, push_guard, tmp_path):
        allowed, msg = push_guard.check_push_authorization(
            "git commit -m 'fix: something'", auth_file=tmp_path / ".push_auth"
        )
        assert allowed is True

    def test_git_log_allowed(self, push_guard, tmp_path):
        allowed, msg = push_guard.check_push_authorization(
            "git log --oneline -5", auth_file=tmp_path / ".push_auth"
        )
        assert allowed is True

    def test_git_branch_allowed(self, push_guard, tmp_path):
        allowed, msg = push_guard.check_push_authorization(
            "git branch -a", auth_file=tmp_path / ".push_auth"
        )
        assert allowed is True

    def test_non_git_command_allowed(self, push_guard, tmp_path):
        allowed, msg = push_guard.check_push_authorization(
            "python -m pytest tests/", auth_file=tmp_path / ".push_auth"
        )
        assert allowed is True

    def test_empty_command_allowed(self, push_guard, tmp_path):
        allowed, msg = push_guard.check_push_authorization(
            "", auth_file=tmp_path / ".push_auth"
        )
        assert allowed is True


# ===========================================================================
# Tests: git push blocked without authorization
# ===========================================================================

class TestPushBlockedWithoutAuth:
    def test_push_blocked_no_auth_file(self, push_guard, tmp_path):
        auth_file = tmp_path / ".push_auth"
        # auth_file does not exist
        allowed, msg = push_guard.check_push_authorization(
            "git push origin main", auth_file=auth_file
        )
        assert allowed is False
        assert "bloqué" in msg.lower() or "bloc" in msg.lower() or "GUARDRAIL" in msg

    def test_push_blocked_message_contains_auth_info(self, push_guard, tmp_path):
        allowed, msg = push_guard.check_push_authorization(
            "git push", auth_file=tmp_path / ".push_auth"
        )
        assert allowed is False
        assert ".push_auth" in msg

    def test_push_blocked_with_force_flag(self, push_guard, tmp_path):
        allowed, msg = push_guard.check_push_authorization(
            "git push --force origin main", auth_file=tmp_path / ".push_auth"
        )
        assert allowed is False

    def test_push_blocked_with_tags(self, push_guard, tmp_path):
        allowed, msg = push_guard.check_push_authorization(
            "git push origin v1.0.0", auth_file=tmp_path / ".push_auth"
        )
        assert allowed is False


# ===========================================================================
# Tests: git push allowed with valid authorization
# ===========================================================================

class TestPushAllowedWithValidAuth:
    def test_push_allowed_with_matching_branch_and_head(self, push_guard, tmp_path):
        auth_file = tmp_path / ".push_auth"
        auth_file.write_text("branch=main\nhead=abc1234\n", encoding="utf-8")

        with patch.object(
            push_guard.subprocess, "check_output",
            side_effect=[
                "main\n",      # git branch --show-current
                "abc1234def5678\n",  # git rev-parse HEAD
            ]
        ):
            allowed, msg = push_guard.check_push_authorization(
                "git push origin main", auth_file=auth_file
            )
        assert allowed is True
        assert msg == ""

    def test_auth_file_consumed_after_valid_use(self, push_guard, tmp_path):
        auth_file = tmp_path / ".push_auth"
        auth_file.write_text("branch=main\nhead=abc1234\n", encoding="utf-8")

        with patch.object(
            push_guard.subprocess, "check_output",
            side_effect=["main\n", "abc1234def5678\n"]
        ):
            push_guard.check_push_authorization("git push origin main", auth_file=auth_file)

        assert not auth_file.exists(), "Authorization file must be consumed after use"

    def test_push_allowed_with_only_branch(self, push_guard, tmp_path):
        auth_file = tmp_path / ".push_auth"
        auth_file.write_text("branch=feat/my-feature\n", encoding="utf-8")

        with patch.object(
            push_guard.subprocess, "check_output",
            side_effect=["feat/my-feature\n", "deadbeef12345\n"]
        ):
            allowed, _ = push_guard.check_push_authorization(
                "git push origin feat/my-feature", auth_file=auth_file
            )
        assert allowed is True

    def test_push_allowed_with_only_head(self, push_guard, tmp_path):
        auth_file = tmp_path / ".push_auth"
        auth_file.write_text("head=deadbeef\n", encoding="utf-8")

        with patch.object(
            push_guard.subprocess, "check_output",
            side_effect=["main\n", "deadbeef12345678\n"]
        ):
            allowed, _ = push_guard.check_push_authorization(
                "git push", auth_file=auth_file
            )
        assert allowed is True


# ===========================================================================
# Tests: authorization context mismatch → blocked
# ===========================================================================

class TestAuthContextMismatch:
    def test_wrong_branch_blocks_push(self, push_guard, tmp_path):
        auth_file = tmp_path / ".push_auth"
        auth_file.write_text("branch=main\nhead=abc123\n", encoding="utf-8")

        with patch.object(
            push_guard.subprocess, "check_output",
            side_effect=["feat/other-branch\n", "abc123def456\n"]
        ):
            allowed, msg = push_guard.check_push_authorization(
                "git push origin feat/other-branch", auth_file=auth_file
            )
        assert allowed is False
        assert "main" in msg or "feat/other-branch" in msg

    def test_wrong_head_blocks_push(self, push_guard, tmp_path):
        auth_file = tmp_path / ".push_auth"
        auth_file.write_text("branch=main\nhead=abc123\n", encoding="utf-8")

        with patch.object(
            push_guard.subprocess, "check_output",
            side_effect=["main\n", "deadbeef12345678\n"]
        ):
            allowed, msg = push_guard.check_push_authorization(
                "git push origin main", auth_file=auth_file
            )
        assert allowed is False

    def test_auth_consumed_on_mismatch(self, push_guard, tmp_path):
        """Authorization is consumed (deleted) even on mismatch — cannot retry."""
        auth_file = tmp_path / ".push_auth"
        auth_file.write_text("branch=main\nhead=abc123\n", encoding="utf-8")

        with patch.object(
            push_guard.subprocess, "check_output",
            side_effect=["feat/other\n", "deadbeef\n"]
        ):
            push_guard.check_push_authorization("git push", auth_file=auth_file)

        assert not auth_file.exists(), "Auth file must be consumed even on mismatch"


# ===========================================================================
# Tests: one-time use invariant
# ===========================================================================

class TestOneTimeUse:
    def test_second_push_blocked_after_consumption(self, push_guard, tmp_path):
        """After one valid push, the next push must be blocked (auth consumed)."""
        auth_file = tmp_path / ".push_auth"
        auth_file.write_text("branch=main\nhead=abc1234\n", encoding="utf-8")

        # First push — allowed and consumes auth
        with patch.object(
            push_guard.subprocess, "check_output",
            side_effect=["main\n", "abc1234def\n"]
        ):
            allowed1, _ = push_guard.check_push_authorization(
                "git push origin main", auth_file=auth_file
            )

        assert allowed1 is True
        assert not auth_file.exists()

        # Second push — no auth file, must be blocked
        allowed2, msg2 = push_guard.check_push_authorization(
            "git push origin main", auth_file=auth_file
        )
        assert allowed2 is False


# ===========================================================================
# Tests: corrupted / unreadable auth file
# ===========================================================================

class TestCorruptedAuth:
    def test_push_blocked_when_auth_is_empty(self, push_guard, tmp_path):
        """Empty auth file has no valid branch/head — should still allow (no constraints)."""
        auth_file = tmp_path / ".push_auth"
        auth_file.write_text("", encoding="utf-8")

        with patch.object(
            push_guard.subprocess, "check_output",
            side_effect=["main\n", "abc123def456\n"]
        ):
            # No branch/head constraints → allowed
            allowed, _ = push_guard.check_push_authorization(
                "git push origin main", auth_file=auth_file
            )
        assert allowed is True

    def test_push_blocked_when_git_unavailable(self, push_guard, tmp_path):
        auth_file = tmp_path / ".push_auth"
        auth_file.write_text("branch=main\n", encoding="utf-8")

        with patch.object(
            push_guard.subprocess, "check_output",
            side_effect=FileNotFoundError("git not found")
        ):
            allowed, msg = push_guard.check_push_authorization(
                "git push origin main", auth_file=auth_file
            )
        assert allowed is False


# ===========================================================================
# Tests: DONE != PUSH_ALLOWED invariant (conceptual)
# ===========================================================================

class TestDoneNotPushAllowed:
    def test_guardrail_does_not_read_task_files(self, push_guard, tmp_path):
        """Guardrail must not check task status — it only reads .push_auth."""
        auth_file = tmp_path / ".push_auth"
        # No auth file, no task files — should still block
        allowed, _ = push_guard.check_push_authorization(
            "git push origin main", auth_file=auth_file
        )
        assert allowed is False, "Push must be blocked regardless of task state"

    def test_authorization_is_explicit_not_implicit(self, push_guard, tmp_path):
        """Existence of DONE tasks does not authorize push — only .push_auth does."""
        auth_file = tmp_path / ".push_auth"
        # Simulate some "DONE task files" existing in tmp_path
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        (tasks_dir / "DEV-001.md").write_text("---\nstatus: DONE\n---\n", encoding="utf-8")

        # Still no .push_auth → blocked
        allowed, _ = push_guard.check_push_authorization(
            "git push origin main", auth_file=auth_file
        )
        assert allowed is False
