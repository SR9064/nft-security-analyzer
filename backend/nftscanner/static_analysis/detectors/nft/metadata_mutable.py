# =========================================================
# MUTABLE NFT METADATA DETECTOR
# =========================================================

def detect_mutable_metadata(source_code):

    issues = []

    mutable_patterns = [

        "setBaseURI",
        "_setBaseURI",
        "baseTokenURI",
        "_baseTokenURI",
        "setTokenURI",
        "_setTokenURI"

    ]

    freeze_patterns = [

        "freezeMetadata",
        "metadataFrozen",
        "permanentURI"
    ]

    has_mutable_metadata = any(
        pattern in source_code
        for pattern in mutable_patterns
    )

    has_freeze_protection = any(
        pattern in source_code
        for pattern in freeze_patterns
    )

    if (
        has_mutable_metadata
        and not has_freeze_protection
    ):

        issues.append({
            "type": "Mutable NFT Metadata Risk",
            "severity": "MEDIUM",
            "line": "N/A"
        })

    return issues
