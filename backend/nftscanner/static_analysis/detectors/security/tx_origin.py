# =========================================================
# TX.ORIGIN DETECTOR
# =========================================================

def detect_tx_origin(source_code):

    issues = []

    if "tx.origin" in source_code:

        issues.append({
            "type": "Unsafe tx.origin Authentication",
            "severity": "High",
            "line": "N/A"
        })

    return issues
