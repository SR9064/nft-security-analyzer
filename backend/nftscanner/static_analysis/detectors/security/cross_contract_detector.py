import re


# ---------------------------------
# Extract contracts + functions + calls
# ---------------------------------
def extract_contracts(source_code):
    contracts = {}
    var_map = {}  # 🔥 variable → contract mapping

    current_contract = None
    current_function = None

    for line in source_code.split("\n"):
        line = line.strip()

        # -----------------------------
        # Detect contract
        # -----------------------------
        contract_match = re.match(r"contract\s+(\w+)", line)
        if contract_match:
            current_contract = contract_match.group(1)
            contracts[current_contract] = {}
            continue

        # -----------------------------
        # Detect variable declarations
        # Example: B b;
        # -----------------------------
        var_match = re.match(r"(\w+)\s+(\w+);", line)
        if var_match:
            contract_type, var_name = var_match.groups()
            var_map[var_name] = contract_type

        # -----------------------------
        # Detect function
        # -----------------------------
        func_match = re.match(r"function\s+(\w+)", line)
        if func_match and current_contract:
            current_function = func_match.group(1)
            contracts[current_contract][current_function] = []
            continue

        # -----------------------------
        # Detect external calls
        # Example: b.fallbackCall()
        # -----------------------------
        if current_contract and current_function:
            matches = re.findall(r"(\w+)\.(\w+)\(", line)

            for var, func in matches:
                # 🔥 Convert variable → contract name
                target_contract = var_map.get(var, var)

                contracts[current_contract][current_function].append(
                    f"{target_contract}.{func}"
                )

    return contracts


# ---------------------------------
# Detect function-level reentrancy cycles
# ---------------------------------
def detect_cross_reentrancy(contracts):
    graph = {}

    # Build graph: Contract.Function → Contract.Function
    for contract, funcs in contracts.items():
        for func, calls in funcs.items():
            node = f"{contract}.{func}"
            graph[node] = calls

    visited = set()
    stack = []
    cycles = []
    issues = []

    def dfs(node):
        if node in stack:
            cycle = stack[stack.index(node):] + [node]
            cycles.append(cycle)
            return

        if node in visited:
            return

        visited.add(node)
        stack.append(node)

        for neighbor in graph.get(node, []):
            dfs(neighbor)

        stack.pop()

    for node in graph:
        dfs(node)

    # ---------------------------------
    # Convert cycles → issues
    # ---------------------------------
    for cycle in cycles:

        issues.append({

            "type":
                (
                    "Multi-Contract "
                    f"Reentrancy Cycle: "
                    f"{' → '.join(cycle)}"
                ),

            "severity":
                "HIGH",

            "path":
                cycle,

            "description":
                (
                    "Multiple contracts form "
                    "a recursive execution cycle "
                    "that may enable reentrancy."
                ),

            "example":
                (
                    "A.withdraw() → "
                    "B.trigger() → "
                    "C.execute() → "
                    "A.withdraw()"
                ),

            "recommendation":
                (
                    "Use reentrancy guards and "
                    "follow checks-effects-"
                    "interactions pattern."
                )
        })

    return issues
