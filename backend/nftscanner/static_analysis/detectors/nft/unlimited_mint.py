# =========================================================
# UNLIMITED MINT DETECTOR
# =========================================================

def detect_unlimited_mint(source_code):

    issues = []

    mint_keywords = [

        "function mint",
        "_mint("

    ]

    supply_protection = [

        "MAX_SUPPLY",
        "maxSupply",
        "totalSupply",
        "currentSupply"
    ]

    has_mint = any(
        keyword in source_code
        for keyword in mint_keywords
    )

    has_supply_limit = any(
        keyword in source_code
        for keyword in supply_protection
    )

    if has_mint and not has_supply_limit:

        issues.append({
            "type": "Unlimited NFT Minting Risk",
            "severity": "HIGH",
            "line": "N/A"
        })

    return issues
