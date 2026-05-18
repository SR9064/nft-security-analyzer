from z3 import Solver, sat


def is_feasible(state):
    s = Solver()

    for cond in state.path_constraints:
        s.add(cond)

    return s.check() == sat
