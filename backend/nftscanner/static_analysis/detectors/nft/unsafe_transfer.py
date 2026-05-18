# =========================================================
# ERC721 UNSAFE TRANSFER DETECTOR
# =========================================================

def detect_unsafe_transfer(source_code):

    issues = []

    has_transfer = (
        "transferFrom(" in source_code
    )

    has_safe_transfer = (
        "safeTransferFrom(" in source_code
    )

    if (
        has_transfer
        and not has_safe_transfer
    ):

        issues.append({
            "type": "Unsafe ERC721 Transfer Usage",
            "severity": "HIGH",
            "line": "N/A"
        })

    return issues
