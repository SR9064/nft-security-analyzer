# =========================================================
# TX.ORIGIN DETECTOR
# =========================================================

def detect_tx_origin(source_code):

    issues = []

    if "tx.origin" in source_code:

        issues.append({

            "type":
                "Unsafe tx.origin Authentication",

            "severity":
                "HIGH",

            "line":
                "N/A",

            "description":
                (
                    "Using tx.origin for "
                    "authentication can allow "
                    "phishing-based attacks."
                ),

            "example":
                (
                    "require(tx.origin == owner);"
                ),

            "recommendation":
                (
                    "Use msg.sender instead "
                    "of tx.origin for "
                    "authorization."
                )
        })

    return issues
