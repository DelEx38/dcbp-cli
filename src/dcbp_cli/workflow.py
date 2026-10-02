"""
DCBP Workflow Engine — deterministic task state machine.

Provides WorkflowState enum, valid transitions, and guard functions.
No I/O, no side-effects — pure state logic only.
"""
from enum import Enum


class WorkflowState(str, Enum):
    """Ordered lifecycle states for a DCBP task."""
    REQUEST      = "REQUEST"
    CLARIFYING   = "CLARIFYING"
    READY        = "READY"
    IMPLEMENTING = "IMPLEMENTING"
    VERIFYING    = "VERIFYING"
    DONE         = "DONE"
    BLOCKED      = "BLOCKED"


# Allowed transitions: from_state → {valid next states}
VALID_TRANSITIONS: dict[str, frozenset] = {
    WorkflowState.REQUEST:      frozenset({WorkflowState.CLARIFYING, WorkflowState.READY}),
    WorkflowState.CLARIFYING:   frozenset({WorkflowState.READY, WorkflowState.BLOCKED}),
    WorkflowState.READY:        frozenset({WorkflowState.IMPLEMENTING}),
    WorkflowState.IMPLEMENTING: frozenset({WorkflowState.VERIFYING, WorkflowState.BLOCKED}),
    WorkflowState.VERIFYING:    frozenset({
        WorkflowState.DONE,
        WorkflowState.IMPLEMENTING,
        WorkflowState.BLOCKED,
    }),
    WorkflowState.BLOCKED:      frozenset({
        WorkflowState.REQUEST,
        WorkflowState.CLARIFYING,
        WorkflowState.READY,
        WorkflowState.IMPLEMENTING,
        WorkflowState.VERIFYING,
    }),
    WorkflowState.DONE:         frozenset(),   # terminal — no outgoing transitions
}

# States from which /dev may start execution
DEV_ENTRY_STATES: frozenset = frozenset({WorkflowState.READY})

# States from which /review may run
REVIEW_ENTRY_STATES: frozenset = frozenset({WorkflowState.VERIFYING})

# The only state that permits DONE transition (/review owns this)
VERIFYING_TO_DONE_GUARD = WorkflowState.VERIFYING


def is_valid_transition(
    from_state: "WorkflowState | str",
    to_state: "WorkflowState | str",
) -> bool:
    """Return True iff the transition from_state → to_state is allowed."""
    try:
        f = WorkflowState(from_state)
        t = WorkflowState(to_state)
    except ValueError:
        return False
    return t in VALID_TRANSITIONS.get(f, frozenset())


def can_dev_start(state: "WorkflowState | str") -> bool:
    """Return True iff /dev may begin execution on a task in this state."""
    try:
        return WorkflowState(state) in DEV_ENTRY_STATES
    except ValueError:
        return False


def can_review_start(state: "WorkflowState | str") -> bool:
    """Return True iff /review may run on a task in this state."""
    try:
        return WorkflowState(state) in REVIEW_ENTRY_STATES
    except ValueError:
        return False
