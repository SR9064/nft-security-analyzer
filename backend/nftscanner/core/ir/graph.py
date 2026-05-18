from graphviz import Digraph


def draw_call_graph(contracts, cycles=None):
    dot = Digraph(comment="Function-Level Call Graph")

    # -------------------------------
    # Nodes + Edges (FUNCTION LEVEL)
    # -------------------------------
    for contract, funcs in contracts.items():
        for func, calls in funcs.items():
            node = f"{contract}.{func}"
            dot.node(node)

            for callee in calls:
                dot.edge(node, callee)

    # -------------------------------
    # Highlight cycles (RED)
    # -------------------------------
    if cycles:
        for cycle in cycles:
            for i in range(len(cycle) - 1):
                dot.edge(
                    cycle[i],
                    cycle[i + 1],
                    color="red",
                    penwidth="2"
                )

    dot.render("call_graph", format="png", cleanup=True)
    print("📊 Function-level graph generated: call_graph.png")
