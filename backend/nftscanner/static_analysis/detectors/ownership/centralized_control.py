# =========================================================
# CENTRALIZED OWNER CONTROL DETECTOR
# =========================================================

def detect_centralized_control(source_code):

    issues = []

    dangerous_admin_functions = [

        "pause(",
        "unpause(",
        "blacklist(",
        "setBlacklist(",
        "withdraw(",
        "emergencyWithdraw(",
        "mint(",
        "burn(",
        "freeze("

    ]

    owner_patterns = [

        "onlyOwner",
        "ownerOnly",
        "msg.sender == owner"
    ]

    has_admin_power = any(
        pattern in source_code
        for pattern in dangerous_admin_functions
    )

    has_owner_control = any(
        pattern in source_code
        for pattern in owner_patterns
    )

    if (
        has_admin_power
        and has_owner_control
    ):

        issues.append({
            "type": "Centralized Owner Privileges",
            "severity": "MEDIUM",
            "line": "N/A"
        })

    return issues
