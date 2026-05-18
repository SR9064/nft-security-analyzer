# =========================================================
# APPROVAL-FOR-ALL ABUSE DETECTOR
# =========================================================

def detect_approval_abuse(source_code):

    issues = []

    approval_patterns = [

        "setApprovalForAll",
        "_setApprovalForAll",
        "approve("

    ]

    suspicious_patterns = [

        "true",
        "operator",
        "msg.sender"
    ]

    has_approval_logic = any(
        pattern in source_code
        for pattern in approval_patterns
    )

    has_suspicious_behavior = any(
        pattern in source_code
        for pattern in suspicious_patterns
    )

    if (
        has_approval_logic
        and has_suspicious_behavior
    ):

        issues.append({
            "type": "Approval For All Abuse Risk",
            "severity": "HIGH",
            "line": "N/A"
        })

    return issues
