from nftscanner.symbolic_execution.executor.explainer import (
    explain_instruction
)

import re
from collections import defaultdict

from nftscanner.core.ir.cfg_builder import build_cfg

from nftscanner.symbolic_execution.executor.tracer import (
    ExecutionTracer
)

from nftscanner.symbolic_execution.validation.reentrancy import (
    validate_reentrancy
)

from z3 import (
    Solver,
    Int,
    IntVal,
    And,
    Or,
    sat
)


# =========================================================
# SYMBOLIC EXPRESSION ENGINE
# =========================================================
class SymbolicExpressionEngine:

    def get_var(self, name):

        return Int(str(name))

    def parse(self, expr):

        expr = str(expr).strip()

        if expr.startswith("(") and expr.endswith(")"):

            expr = expr[1:-1].strip()

        # -------------------------------------------------
        # LOGICAL AND
        # -------------------------------------------------
        if "&&" in expr:

            return And(
                *[
                    self.parse(e.strip())
                    for e in expr.split("&&")
                ]
            )

        # -------------------------------------------------
        # LOGICAL OR
        # -------------------------------------------------
        if "||" in expr:

            return Or(
                *[
                    self.parse(e.strip())
                    for e in expr.split("||")
                ]
            )

        # -------------------------------------------------
        # COMPARISON
        # -------------------------------------------------
        match = re.match(
            r"(.+?)(==|!=|>=|<=|>|<)(.+)",
            expr
        )

        if match:

            l, op, r = match.groups()

            l = l.strip()
            r = r.strip()

            # ---------------------------------------------
            # LEFT OPERAND
            # ---------------------------------------------
            if l == "msg.sender":

                L = Int("msg_sender")

            elif l.isdigit():

                L = IntVal(int(l))

            else:

                L = self.get_var(l)

            # ---------------------------------------------
            # RIGHT OPERAND
            # ---------------------------------------------
            if r == "msg.sender":

                R = Int("msg_sender")

            elif r.isdigit():

                R = IntVal(int(r))

            else:

                R = self.get_var(r)

            return {
                "==": L == R,
                "!=": L != R,
                ">": L > R,
                "<": L < R,
                ">=": L >= R,
                "<=": L <= R
            }[op]

        # -------------------------------------------------
        # BOOLEAN VARIABLE
        # -------------------------------------------------
        if expr.isidentifier():

            return self.get_var(expr) != 0

        return self.get_var(expr) != 0


# =========================================================
# EVM STATE
# =========================================================
class EVMState:

    def __init__(self, pid="root"):

        self.solver = Solver()

        self.path_id = pid

        self.storage = {}

        self.balance = defaultdict(
            lambda: Int("bal")
        )

        # -------------------------------------------------
        # TAINT TRACKING
        # -------------------------------------------------
        self.tainted = set()

        self.taint_flow = []

        # -------------------------------------------------
        # EXPLOIT TRACE
        # -------------------------------------------------
        self.exploit_chain = []

        # -------------------------------------------------
        # SYMBOLIC CALLER MODEL
        # -------------------------------------------------
        self.msg_sender = Int(
            "msg_sender"
        )

        self.attacker = Int(
            "attacker"
        )

        self.solver.add(
            self.msg_sender
            == self.attacker
        )

        self.locked = False

        self.call_stack = []

        self.exploit_path = []

        self.contract_trace = []

        self.visited = set()

        self.state_written_after_call = False

        self.external_call_seen = False

        self.last_owner_change = None

        self.last_balance_change = None

        self.owner_history = defaultdict(list)

    # =====================================================
    # FORK STATE (OPTIMIZED)
    # =====================================================
    def fork(self):

        new = EVMState(
            pid=self.path_id + "->fork"
        )

        # -------------------------------------------------
        # SAFE SOLVER COPY
        # -------------------------------------------------
        new.solver = Solver()

        new.solver.add(
            self.solver.assertions()
        )

        # -------------------------------------------------
        # LIGHTWEIGHT STATE COPY
        # -------------------------------------------------
        new.storage = dict(
            self.storage
        )

        new.balance = defaultdict(
            lambda: Int("bal"),
            self.balance
        )

        new.tainted = set(
            self.tainted
        )

        new.taint_flow = list(
            self.taint_flow
        )

        new.exploit_chain = list(
            self.exploit_chain
        )

        new.call_stack = list(
            self.call_stack
        )

        new.exploit_path = list(
            self.exploit_path
        )

        new.contract_trace = list(
            self.contract_trace
        )

        new.visited = set()

        new.state_written_after_call = (
            self.state_written_after_call
        )

        new.external_call_seen = (
            self.external_call_seen
        )

        new.last_owner_change = (
            self.last_owner_change
        )

        new.last_balance_change = (
            self.last_balance_change
        )

        new.owner_history = defaultdict(
            list,
            {
                k: list(v)
                for k, v in self.owner_history.items()
            }
        )

        return new


# =========================================================
# EXECUTOR
# =========================================================
class Executor:

    def __init__(self, ir):

        self.ir = ir

        self.cfg = None

        self.vulns = []

        self.seen_vulns = set()

        self.seen_traces = set()

        self.sym = SymbolicExpressionEngine()

        self.tracer = ExecutionTracer()

        self.max_steps = 300

    # =====================================================
    # RUN ENGINE
    # =====================================================
    def run(self):

        print("\n[SIMULATOR] Building CFG...\n")

        self.cfg = build_cfg(self.ir)

        state = EVMState()

        print("[SIMULATOR] Execution started...\n")

        if self.cfg:

            for node in self.cfg.nodes.values():

                if (
                    node.statements.get("type")
                    == "FUNCTION"
                ):

                    self.execute(
                        node,
                        state.fork()
                    )

        print("\n[SIMULATOR] Execution finished\n")

        self.tracer.export_dot(
            "trace.dot"
        )

        return self.vulns

    # =====================================================
    # EXECUTE CFG
    # =====================================================
    def execute(self, start_node, state):

        queue = [start_node]

        step_counter = 0

        while queue:

            step_counter += 1

            # -------------------------------------------------
            # EXECUTION LIMIT
            # -------------------------------------------------
            if step_counter > self.max_steps:

                print(
                    "[PATH BLOCKED] Symbolic execution limit reached"
                )

                break

            node = queue.pop(0)

            visit_key = (
                f"{node.id}:{state.path_id}"
            )

            if visit_key in state.visited:

                continue

            state.visited.add(
                visit_key
            )

            t = node.statements.get(
                "type"
            )

            # -------------------------------------------------
            # HUMAN TRACE
            # -------------------------------------------------
            human_text = explain_instruction(
                t,
                node.statements
            )

            if human_text:

                if (
                    human_text
                    not in self.seen_traces
                ):

                    self.seen_traces.add(
                        human_text
                    )

                    print(
                        f"[TRACE] {human_text}"
                    )

                    self.tracer.log_node(
                        node.id,
                        human_text
                    )

            # -------------------------------------------------
            # TRACE EDGES
            # -------------------------------------------------
            for e in node.edges:

                self.tracer.add_edge(
                    node.id,
                    e.id
                )

            # =================================================
            # FUNCTION
            # =================================================
            if t == "FUNCTION":

                pass

            # =================================================
            # STORAGE WRITE
            # =================================================
            elif t == "SSTORE":

                key = node.statements.get(
                    "key",
                    "unknown"
                )

                value = node.statements.get(
                    "value",
                    "updated"
                )

                state.storage[key] = value

                state.state_written_after_call = True

            # =================================================
            # REQUIRE
            # =================================================
            elif t == "REQUIRE":

                condition = node.statements.get(
                    "condition",
                    "True"
                )

                try:

                    symbolic_condition = (
                        self.sym.parse(
                            condition
                        )
                    )

                    state.solver.add(
                        symbolic_condition
                    )

                    if (
                        state.solver.check()
                        != sat
                    ):

                        print(
                            "[PATH BLOCKED] Requirement failed"
                        )

                        continue

                except Exception as e:

                    print(
                        f"[REQUIRE ERROR] {e}"
                    )

            # =================================================
            # CALL
            # =================================================
            elif t == "CALL":

                target = node.statements.get(
                    "target",
                    "UNKNOWN"
                )

                # -------------------------------------------------
                # RECURSION BLOCK
                # -------------------------------------------------
                if target in state.call_stack:

                    print(
                        f"[PATH BLOCKED] Recursive call prevented → {target}"
                    )

                    continue

                state.exploit_chain.append(
                    target
                )

                state.call_stack.append(
                    target
                )

                state.exploit_path.append(
                    f"CALL:{target}"
                )

                if "." in target:

                    state.contract_trace.append(
                        target.split(".")[0]
                    )

                state.external_call_seen = True

            # =================================================
            # REENTRY
            # =================================================
            elif t == "REENTRY":

                target = node.statements.get(
                    "target",
                    "UNKNOWN"
                )

                recursive = (
                    target
                    in state.call_stack
                )

                if (
                    recursive
                    and state.external_call_seen
                    and state.state_written_after_call
                ):

                    if validate_reentrancy(
                        state
                    ):

                        sig = (
                            f"REENTRANCY:{target}"
                        )

                        if (
                            sig
                            not in self.seen_vulns
                        ):

                            self.seen_vulns.add(
                                sig
                            )

                            self.vulns.append({

                                "type":
                                "REENTRANCY",

                                "severity":
                                "CRITICAL",

                                "target":
                                target,

                                "exploit_chain":
                                state.exploit_chain.copy(),

                                "attack_flow":
                                " → ".join(
                                    state.exploit_chain
                                )
                            })

            # =================================================
            # NEXT NODES
            # =================================================
            for edge in node.edges:

                if edge:

                    queue.append(edge)

            # -------------------------------------------------
            # POP CALL STACK
            # -------------------------------------------------
            if (
                t == "CALL"
                and state.call_stack
            ):

                state.call_stack.pop()


# =========================================================
# API
# =========================================================
def run_evm(ir):

    ex = Executor(ir)

    res = ex.run()

    print("\n=== EVM SIMULATION RESULT ===")

    print("VULNS:", res)

    return res
