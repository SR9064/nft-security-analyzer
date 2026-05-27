# =========================================================
# UNCHECKED EXTERNAL CALL DETECTOR
# =========================================================

def detect_unchecked_call(source_code):

    issues = []

    dangerous_patterns = [

        ".call(",
        ".call{",
        ".send("

    ]

    for pattern in dangerous_patterns:

        if pattern in source_code:

            issues.append({

                "type":
                    "Unchecked External Call",

                "severity":
                    "HIGH",

                "line":
                    "N/A",

                "description":
                    (
                        "Low-level external calls "
                        "are executed without "
                        "checking success status."
                    ),

                "example":
                    (
                        "(bool success,) = "
                        "target.call(data);\n"
                        "// success ignored"
                    ),

                "recommendation":
                    (
                        "Always validate external "
                        "call return values using "
                        "require(success)."
                    )
            })

            break

    return issues
