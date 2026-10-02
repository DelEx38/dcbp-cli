"""
Tests for DCBP Workflow Engine — state machine, transitions, guards.
"""
import pytest
from dcbp_cli.workflow import (
    WorkflowState,
    VALID_TRANSITIONS,
    is_valid_transition,
    can_dev_start,
    can_review_start,
    DEV_ENTRY_STATES,
    REVIEW_ENTRY_STATES,
)


# ===========================================================================
# Tests: WorkflowState enum
# ===========================================================================

class TestWorkflowState:
    def test_all_states_exist(self):
        expected = {"REQUEST", "CLARIFYING", "READY", "IMPLEMENTING", "VERIFYING", "DONE", "BLOCKED"}
        actual = {s.value for s in WorkflowState}
        assert actual == expected

    def test_state_is_str_subclass(self):
        assert isinstance(WorkflowState.READY, str)

    def test_state_from_string(self):
        assert WorkflowState("READY") == WorkflowState.READY

    def test_invalid_state_raises(self):
        with pytest.raises(ValueError):
            WorkflowState("INVALID")

    def test_done_is_terminal(self):
        assert VALID_TRANSITIONS[WorkflowState.DONE] == frozenset()


# ===========================================================================
# Tests: Valid transitions
# ===========================================================================

class TestValidTransitions:
    # REQUEST transitions
    def test_request_to_clarifying(self):
        assert is_valid_transition("REQUEST", "CLARIFYING")

    def test_request_to_ready(self):
        assert is_valid_transition("REQUEST", "READY")

    def test_request_cannot_go_to_implementing(self):
        assert not is_valid_transition("REQUEST", "IMPLEMENTING")

    def test_request_cannot_go_to_done(self):
        assert not is_valid_transition("REQUEST", "DONE")

    # CLARIFYING transitions
    def test_clarifying_to_ready(self):
        assert is_valid_transition("CLARIFYING", "READY")

    def test_clarifying_to_blocked(self):
        assert is_valid_transition("CLARIFYING", "BLOCKED")

    def test_clarifying_cannot_go_to_implementing(self):
        assert not is_valid_transition("CLARIFYING", "IMPLEMENTING")

    # READY transitions
    def test_ready_to_implementing(self):
        assert is_valid_transition("READY", "IMPLEMENTING")

    def test_ready_cannot_go_to_verifying(self):
        assert not is_valid_transition("READY", "VERIFYING")

    def test_ready_cannot_go_to_done(self):
        assert not is_valid_transition("READY", "DONE")

    # IMPLEMENTING transitions
    def test_implementing_to_verifying(self):
        assert is_valid_transition("IMPLEMENTING", "VERIFYING")

    def test_implementing_to_blocked(self):
        assert is_valid_transition("IMPLEMENTING", "BLOCKED")

    def test_implementing_cannot_go_to_done(self):
        assert not is_valid_transition("IMPLEMENTING", "DONE")

    def test_implementing_cannot_go_to_ready(self):
        assert not is_valid_transition("IMPLEMENTING", "READY")

    # VERIFYING transitions
    def test_verifying_to_done(self):
        assert is_valid_transition("VERIFYING", "DONE")

    def test_verifying_to_implementing(self):
        assert is_valid_transition("VERIFYING", "IMPLEMENTING")

    def test_verifying_to_blocked(self):
        assert is_valid_transition("VERIFYING", "BLOCKED")

    def test_verifying_cannot_go_to_ready(self):
        assert not is_valid_transition("VERIFYING", "READY")

    # DONE is terminal
    def test_done_has_no_valid_next_states(self):
        for state in WorkflowState:
            if state != WorkflowState.DONE:
                assert not is_valid_transition("DONE", state.value)

    # BLOCKED can recover to most states
    def test_blocked_to_ready(self):
        assert is_valid_transition("BLOCKED", "READY")

    def test_blocked_to_implementing(self):
        assert is_valid_transition("BLOCKED", "IMPLEMENTING")

    def test_blocked_to_verifying(self):
        assert is_valid_transition("BLOCKED", "VERIFYING")

    def test_blocked_cannot_go_to_done(self):
        assert not is_valid_transition("BLOCKED", "DONE")


# ===========================================================================
# Tests: is_valid_transition edge cases
# ===========================================================================

class TestIsValidTransitionEdgeCases:
    def test_invalid_from_state_returns_false(self):
        assert not is_valid_transition("BOGUS", "READY")

    def test_invalid_to_state_returns_false(self):
        assert not is_valid_transition("READY", "BOGUS")

    def test_both_invalid_returns_false(self):
        assert not is_valid_transition("X", "Y")

    def test_accepts_enum_values(self):
        assert is_valid_transition(WorkflowState.READY, WorkflowState.IMPLEMENTING)

    def test_accepts_mixed_types(self):
        assert is_valid_transition("READY", WorkflowState.IMPLEMENTING)


# ===========================================================================
# Tests: /dev guard
# ===========================================================================

class TestDevGuard:
    def test_dev_can_start_from_ready(self):
        assert can_dev_start("READY")

    def test_dev_cannot_start_from_request(self):
        assert not can_dev_start("REQUEST")

    def test_dev_cannot_start_from_clarifying(self):
        assert not can_dev_start("CLARIFYING")

    def test_dev_cannot_start_from_implementing(self):
        """IMPLEMENTING is for resume, not fresh start — guard is for READY only."""
        assert not can_dev_start("IMPLEMENTING")

    def test_dev_cannot_start_from_verifying(self):
        assert not can_dev_start("VERIFYING")

    def test_dev_cannot_start_from_done(self):
        assert not can_dev_start("DONE")

    def test_dev_cannot_start_from_blocked(self):
        assert not can_dev_start("BLOCKED")

    def test_dev_invalid_state_returns_false(self):
        assert not can_dev_start("NOT_A_STATE")

    def test_dev_entry_states_constant(self):
        assert WorkflowState.READY in DEV_ENTRY_STATES


# ===========================================================================
# Tests: /review guard
# ===========================================================================

class TestReviewGuard:
    def test_review_can_start_from_verifying(self):
        assert can_review_start("VERIFYING")

    def test_review_cannot_start_from_implementing(self):
        assert not can_review_start("IMPLEMENTING")

    def test_review_cannot_start_from_ready(self):
        assert not can_review_start("READY")

    def test_review_cannot_start_from_done(self):
        assert not can_review_start("DONE")

    def test_review_invalid_state_returns_false(self):
        assert not can_review_start("BOGUS")

    def test_review_entry_states_constant(self):
        assert WorkflowState.VERIFYING in REVIEW_ENTRY_STATES


# ===========================================================================
# Tests: Lifecycle contracts
# ===========================================================================

class TestLifecycleContracts:
    def test_dev_enters_implementing(self):
        """READY → IMPLEMENTING is the /dev entry transition."""
        assert is_valid_transition("READY", "IMPLEMENTING")

    def test_dev_exits_to_verifying(self):
        """IMPLEMENTING → VERIFYING is the /dev exit transition."""
        assert is_valid_transition("IMPLEMENTING", "VERIFYING")

    def test_dev_cannot_reach_done(self):
        """IMPLEMENTING → DONE is forbidden — /review owns DONE."""
        assert not is_valid_transition("IMPLEMENTING", "DONE")

    def test_review_owns_done_transition(self):
        """VERIFYING → DONE is the only path to DONE."""
        reachable_from_done = [
            s for s in WorkflowState
            if is_valid_transition(s, WorkflowState.DONE)
        ]
        assert reachable_from_done == [WorkflowState.VERIFYING]

    def test_full_happy_path_is_valid(self):
        """REQUEST → CLARIFYING → READY → IMPLEMENTING → VERIFYING → DONE."""
        path = [
            ("REQUEST", "CLARIFYING"),
            ("CLARIFYING", "READY"),
            ("READY", "IMPLEMENTING"),
            ("IMPLEMENTING", "VERIFYING"),
            ("VERIFYING", "DONE"),
        ]
        for from_s, to_s in path:
            assert is_valid_transition(from_s, to_s), f"{from_s} → {to_s} should be valid"

    def test_review_failure_path_is_valid(self):
        """VERIFYING → IMPLEMENTING (correction needed)."""
        assert is_valid_transition("VERIFYING", "IMPLEMENTING")

    def test_blocked_recovery_path(self):
        """IMPLEMENTING → BLOCKED → IMPLEMENTING (unblocked)."""
        assert is_valid_transition("IMPLEMENTING", "BLOCKED")
        assert is_valid_transition("BLOCKED", "IMPLEMENTING")
