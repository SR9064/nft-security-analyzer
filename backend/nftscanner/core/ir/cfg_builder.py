from collections import defaultdict


# =========================================================
# CFG NODE
# =========================================================
class CFGNode:

    def __init__(self, node_id, statements=None, contract=None):

        self.id = node_id

        self.statements = statements or {}

        self.edges = []

        self.contract = contract

    def connect(self, other):

        self.edges.append(other)


# =========================================================
# CFG STRUCTURE
# =========================================================
class CFG:

    def __init__(self):

        self.nodes = {}

        self.entry = None

        self.call_graph = defaultdict(set)

        self.contract_map = defaultdict(list)


# =========================================================
# BUILD CFG
# =========================================================
def build_cfg(ir):

    cfg = CFG()

    node_id = 0

    # -----------------------------------------------------
    # CREATE NODE
    # -----------------------------------------------------
    def new_node(stmt, contract):

        nonlocal node_id

        n = CFGNode(
            node_id,
            stmt,
            contract
        )

        cfg.nodes[node_id] = n

        node_id += 1

        return n

    contracts = ir.get("contracts", [])

    function_entries = {}

    # =====================================================
    # PASS 1 — FUNCTION ENTRY NODES
    # =====================================================
    for contract in contracts:

        cname = contract.get(
            "name",
            "Unknown"
        )

        for fn in contract.get(
            "functions",
            []
        ):

            fname = fn.get("name")

            fn_node = new_node(
                {
                    "type": "FUNCTION",
                    "name": fname
                },
                cname
            )

            function_entries[
                (cname, fname)
            ] = fn_node

            cfg.contract_map[
                cname
            ].append(fn_node)

            if cfg.entry is None:

                cfg.entry = fn_node

    # =====================================================
    # PASS 2 — BODY NODES
    # =====================================================
    for contract in contracts:

        cname = contract.get(
            "name",
            "Unknown"
        )

        for fn in contract.get(
            "functions",
            []
        ):

            fname = fn.get("name")

            entry = function_entries[
                (cname, fname)
            ]

            prev = entry

            body = fn.get("body", [])

            # -------------------------------------------------
            # BUILD LINEAR FLOW
            # -------------------------------------------------
            for stmt in body:

                stmt_node = new_node(
                    stmt,
                    cname
                )

                # ---------------------------------------------
                # LINEAR CFG CHAIN
                # ---------------------------------------------
                prev.connect(stmt_node)

                prev = stmt_node

                if not isinstance(stmt, dict):
                    continue

                stype = stmt.get("type")

                target = stmt.get("target")

                # =============================================
                # CALL HANDLING
                # =============================================
                if (
                    stype == "CALL"
                    and isinstance(target, str)
                ):

                    # -----------------------------------------
                    # CROSS CONTRACT CALL
                    # -----------------------------------------
                    if (
                        "." in target
                        and target not in [
                            "require",
                            "assert"
                        ]
                    ):

                        callee_contract, callee_func = (
                            target.split(".", 1)
                        )

                        cfg.call_graph[
                            cname
                        ].add(callee_contract)

                        # -------------------------------------
                        # CONNECT TO REAL FUNCTION ENTRY
                        # -------------------------------------
                        callee_node = function_entries.get(
                            (
                                callee_contract,
                                callee_func
                            )
                        )

                        if callee_node:

                            stmt_node.connect(
                                callee_node
                            )

                        # -------------------------------------
                        # OPTIONAL REENTRY EDGE
                        # -------------------------------------
                        re_node = new_node(
                            {
                                "type": "REENTRY",
                                "target": target
                            },
                            callee_contract
                        )

                        stmt_node.connect(
                            re_node
                        )

                    # -----------------------------------------
                    # INTERNAL CALL
                    # -----------------------------------------
                    else:

                        internal_node = (
                            function_entries.get(
                                (cname, target)
                            )
                        )

                        if internal_node:

                            stmt_node.connect(
                                internal_node
                            )

    return cfg
