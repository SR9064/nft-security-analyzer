# =========================================================
# DELEGATECALL DETECTOR
# =========================================================

def detect_delegatecall(source_code):

    issues = []

    if "delegatecall(" in source_code:

        issues.append({

            "type":
                "Dangerous Delegatecall Usage",

            "severity":
                "HIGH",

            "line":
                "N/A",

            "description":
                (
                    "delegatecall executes "
                    "external code in the "
                    "current contract context."
                ),

            "example":
                (
                    "target.delegatecall(data);"
                ),

            "recommendation":
                (
                    "Avoid delegatecall unless "
                    "strictly required and "
                    "fully validated."
                )
        })

    return issues
