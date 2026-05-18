# =========================================================
# ERC2981 ROYALTY ABUSE DETECTOR
# =========================================================

def detect_royalty_abuse(source_code):

    issues = []

    royalty_patterns = [

        "setRoyalty",
        "_setDefaultRoyalty",
        "royaltyInfo",
        "setTokenRoyalty"

    ]

    protection_patterns = [

        "MAX_ROYALTY",
        "feeDenominator",
        "require(fee",
        "require(royalty"
    ]

    has_royalty_logic = any(
        pattern in source_code
        for pattern in royalty_patterns
    )

    has_royalty_limit = any(
        pattern in source_code
        for pattern in protection_patterns
    )

    if (
        has_royalty_logic
        and not has_royalty_limit
    ):

        issues.append({
            "type": "Royalty Manipulation Risk",
            "severity": "MEDIUM",
            "line": "N/A"
        })

    return issues
