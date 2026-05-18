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
            "type": "Dangerous Selfdestruct Usage",
            "severity": "CRITICAL",
            "line": "N/A"
        })

    return issues
