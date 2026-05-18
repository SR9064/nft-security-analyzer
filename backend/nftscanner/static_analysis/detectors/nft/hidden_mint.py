# =========================================================
# HIDDEN / BACKDOOR MINT DETECTOR
# =========================================================

def detect_hidden_mint(source_code):

    issues = []

    suspicious_mint_patterns = [

        "function mint",
        "_mint(",
        "_safeMint("

    ]

    owner_control_patterns = [

        "onlyOwner",
        "msg.sender == owner"
    ]

    stealth_patterns = [

        "airdrop",
        "reserveMint",
        "teamMint",
        "devMint",
        "adminMint"

    ]

    has_mint_logic = any(
        pattern in source_code
        for pattern in suspicious_mint_patterns
    )

    has_owner_control = any(
        pattern in source_code
        for pattern in owner_control_patterns
    )

    has_stealth_mint = any(
        pattern in source_code
        for pattern in stealth_patterns
    )

    if (
        has_mint_logic
        and (
            has_owner_control
            or has_stealth_mint
        )
    ):

        issues.append({
            "type": "Hidden Owner Mint Capability",
            "severity": "HIGH",
            "line": "N/A"
        })

    return issues
