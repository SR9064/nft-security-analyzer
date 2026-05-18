# -------------------------------------------------
# Helper: Extract function names from AST
# -------------------------------------------------
def extract_functions(ast):

    functions = set()

    def traverse(node):

        if isinstance(node, dict):

            if node.get("type") == "FunctionDefinition":

                name = node.get("name")

                if name:
                    functions.add(name)

            for v in node.values():
                traverse(v)

        elif isinstance(node, list):

            for item in node:
                traverse(item)

    traverse(ast)

    return functions


# -------------------------------------------------
# Compliance Checks
# -------------------------------------------------
def run_compliance_checks(
    ast,
    source_code,
    standards,
    verbose=False
):

    if verbose:

        print(
            "      → [4(i)] Checking NFT Compliance..."
        )

    issues = []

    functions = extract_functions(ast)

    # -------------------------------------------------
    # ERC-721
    # -------------------------------------------------
    if "ERC721" in standards:

        erc721_required = {
            "balanceOf",
            "ownerOf",
            "approve",
            "transferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "getApproved",
            "isApprovedForAll",
            "supportsInterface"
        }

        missing_721 = list(
            erc721_required - functions
        )

        if missing_721:

            issues.append({
                "type":
                f"ERC-721 Missing Functions: {missing_721}",

                "severity": "Low",

                "line": "N/A"
            })

    # -------------------------------------------------
    # ERC-1155
    # -------------------------------------------------
    if "ERC1155" in standards:

        erc1155_required = {
            "safeTransferFrom",
            "safeBatchTransferFrom",
            "balanceOf",
            "balanceOfBatch"
        }

        missing_1155 = list(
            erc1155_required - functions
        )

        if missing_1155:

            issues.append({
                "type":
                f"ERC-1155 Missing Functions: {missing_1155}",

                "severity": "Low",

                "line": "N/A"
            })

    # -------------------------------------------------
    # ERC-2981
    # -------------------------------------------------
    if "ERC2981" in standards:

        if "royaltyInfo" not in functions:

            issues.append({
                "type":
                "ERC-2981 Royalty Function Missing",

                "severity": "Low",

                "line": "N/A"
            })

    return issues
