from z3 import (
    Solver,
    Int,
    Bool,
    And,
    sat
)


# =========================================================
# REENTRANCY VALIDATION
# =========================================================
def validate_reentrancy(state):

    solver = Solver()

    # -----------------------------------------------------
    # SYMBOLIC VARIABLES
    # -----------------------------------------------------
    attacker_gain = Int(
        "attacker_gain"
    )

    contract_loss = Int(
        "contract_loss"
    )

    recursive_call = Bool(
        "recursive_call"
    )

    external_call_seen = Bool(
        "external_call_seen"
    )

    state_write_after_call = Bool(
        "state_write_after_call"
    )

    # -----------------------------------------------------
    # BASIC EXPLOIT CONSTRAINTS
    # -----------------------------------------------------
    solver.add(
        attacker_gain > 0
    )

    solver.add(
        contract_loss > 0
    )

    solver.add(
        attacker_gain
        == contract_loss
    )

    # -----------------------------------------------------
    # RECURSIVE REENTRY REQUIRED
    # -----------------------------------------------------
    solver.add(
        recursive_call == True
    )

    # -----------------------------------------------------
    # MUST HAVE EXTERNAL CALL
    # -----------------------------------------------------
    solver.add(
        external_call_seen
        == state.external_call_seen
    )

    # -----------------------------------------------------
    # MUST WRITE STATE AFTER CALL
    # -----------------------------------------------------
    solver.add(
        state_write_after_call
        == state.state_written_after_call
    )

    # -----------------------------------------------------
    # EXPLOIT CONDITION
    # -----------------------------------------------------
    solver.add(
        And(
            recursive_call,
            external_call_seen,
            state_write_after_call
        )
    )

    # -----------------------------------------------------
    # SAT CHECK
    # -----------------------------------------------------
    if solver.check() == sat:

        return True

    return False
