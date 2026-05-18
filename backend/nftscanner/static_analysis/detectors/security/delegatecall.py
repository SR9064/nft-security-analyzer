# =========================================================
# DELEGATECALL DETECTOR
# =========================================================

def detect_delegatecall(source_code):

    issues = []

    if "delegatecall(" in source_code:

        issues.append({
            "type": "Dangerous Delegatecall Usage",
            "severity": "HIGH",
            "line": "N/A"
        })

    return issues
