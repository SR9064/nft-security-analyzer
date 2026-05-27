# =========================================================
# SELFDESTRUCT DETECTOR
# =========================================================

def detect_selfdestruct(source_code):

    issues = []

    if (
        "selfdestruct(" in source_code
        or "suicide(" in source_code
    ):

        issues.append({

            "type":
                "Dangerous Selfdestruct Usage",

            "severity":
                "CRITICAL",

            "line":
                "N/A",

            "description":
                (
                    "selfdestruct can permanently "
                    "destroy the contract and "
                    "redirect funds."
                ),

            "example":
                (
                    "selfdestruct(payable(owner));"
                ),

            "recommendation":
                (
                    "Avoid selfdestruct in "
                    "production smart contracts."
                )
        })

    return issues
