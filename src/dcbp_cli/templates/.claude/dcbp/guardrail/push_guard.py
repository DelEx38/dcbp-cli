#!/usr/bin/env python3
"""
DCBP push guardrail — blocks 'git push' without explicit authorization.

Invoked as a Claude Code PreToolUse hook on the Bash tool.
Input: JSON on stdin (Claude Code hook format).
Exit 0 → allow. Exit 2 → block.

Authorization file: .claude/dcbp/.push_auth
Format (plain text, key=value):
    branch=<expected-branch>
    head=<expected-HEAD-prefix>

Both fields are optional but recommended.
Authorization is one-time: consumed on first valid use.
"""
import json
import re
import subprocess
import sys
from pathlib import Path


# ── Auth file location (relative to project root) ─────────────────────────────
AUTH_FILE = Path(".claude/dcbp/.push_auth")


def check_push_authorization(
    command: str,
    auth_file: Path = AUTH_FILE,
) -> tuple[bool, str]:
    """
    Check whether `command` is an authorized git push.

    Returns:
        (True, "")            — command is not a push, or push is authorized
        (False, reason_msg)   — push is blocked; reason_msg explains why
    """
    # Only act on git push
    if not re.search(r"\bgit\s+push\b", command):
        return True, ""

    # Authorization file must exist
    if not auth_file.exists():
        return False, (
            "\n\u26d4 DCBP GUARDRAIL: git push bloqué\n"
            "   Aucune autorisation de push trouvée.\n"
            "   Créez .claude/dcbp/.push_auth (voir dcbp doc push-auth).\n"
            "   Format:\n"
            "     branch=<branche>\n"
            "     head=<sha_court>\n"
        )

    # Parse authorization
    try:
        lines = {
            k: v
            for k, _, v in (
                line.partition("=")
                for line in auth_file.read_text(encoding="utf-8").strip().splitlines()
            )
            if k and v
        }
    except OSError:
        auth_file.unlink(missing_ok=True)
        return False, "\u26d4 DCBP GUARDRAIL: .push_auth illisible — autorisation invalide."

    # Read current git state
    try:
        current_branch = subprocess.check_output(
            ["git", "branch", "--show-current"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        current_head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        auth_file.unlink(missing_ok=True)
        return False, "\u26d4 DCBP GUARDRAIL: impossible de lire l'état git."

    auth_branch = lines.get("branch", "")
    auth_head   = lines.get("head", "")

    if auth_branch and auth_branch != current_branch:
        auth_file.unlink(missing_ok=True)
        return False, (
            f"\u26d4 DCBP GUARDRAIL: Push bloqué\n"
            f"   Autorisé pour '{auth_branch}', branche actuelle: '{current_branch}'."
        )

    if auth_head and not current_head.startswith(auth_head):
        auth_file.unlink(missing_ok=True)
        return False, (
            f"\u26d4 DCBP GUARDRAIL: Push bloqué\n"
            f"   Autorisé pour HEAD '{auth_head}', actuel: '{current_head[:8]}'."
        )

    # Valid — consume (one-time use)
    auth_file.unlink(missing_ok=True)
    return True, ""


def main() -> None:
    # Read Claude Code hook input from stdin
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # Unparseable — fail open (don't block non-push tools)

    # Support both flat format {"command": ...} and nested {"tool_input": {"command": ...}}
    tool_input = data.get("tool_input", data)
    command = tool_input.get("command", "")

    allowed, message = check_push_authorization(command)
    if not allowed:
        print(message, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
