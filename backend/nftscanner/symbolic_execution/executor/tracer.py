from collections import defaultdict
import json
import graphviz
import os


class ExecutionTracer:

    def __init__(self):

        self.paths = []

        self.current_path = []

        self.constraints = []

        self.exploits = []

        self.graph = defaultdict(list)

    # -------------------------
    # PATH TRACKING
    # -------------------------
    def log_node(
        self,
        node_id,
        node_type
    ):

        self.current_path.append({
            "node": node_id,
            "type": node_type
        })

    def log_constraint(
        self,
        constraint
    ):

        self.constraints.append(
            str(constraint)
        )

    def branch(self):

        self.paths.append(
            self.current_path
        )

        self.current_path = list(
            self.current_path
        )

    # -------------------------
    # EXPLOIT TRACKING
    # -------------------------
    def log_exploit(
        self,
        path,
        issue
    ):

        self.exploits.append({
            "issue": issue,
            "path": path
        })

    # -------------------------
    # GRAPH BUILDING
    # -------------------------
    def add_edge(
        self,
        a,
        b
    ):

        self.graph[a].append(b)

    # -------------------------
    # EXPORT JSON
    # -------------------------
    def export_json(
        self,
        path="trace.json"
    ):

        with open(path, "w") as f:

            json.dump({

                "paths":
                self.paths,

                "constraints":
                self.constraints,

                "exploits":
                self.exploits

            }, f, indent=2)

        print(
            f"[Tracer] JSON exported → {path}"
        )

    # -------------------------
    # EXPORT DOT + PNG
    # -------------------------
    def export_dot(
        self,
        path="trace.dot"
    ):

        # ---------------------------------
        # WRITE DOT FILE
        # ---------------------------------
        with open(path, "w") as f:

            f.write(
                "digraph ExecutionTrace {\n"
            )

            for a, bs in self.graph.items():

                for b in bs:

                    f.write(
                        f'  "{a}" -> "{b}";\n'
                    )

            f.write("}\n")

        print(
            f"[Tracer] DOT exported → {path}"
        )

        # ---------------------------------
        # GENERATE PNG
        # ---------------------------------
        try:

            dot = graphviz.Source.from_file(path)

            output_path = (
                "output/call_graph"
            )

            dot.render(
                output_path,
                format="png",
                cleanup=True
            )

            print(
                "[Tracer] PNG graph generated → output/call_graph"
            )

        except Exception as e:

            print(
                f"[Tracer] Graph render failed: {e}"
            )
