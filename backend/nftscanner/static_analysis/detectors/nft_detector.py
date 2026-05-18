def detect_nft_standard(ast):
    standards = set()

    # ERC-721 mandatory functions
    erc721_functions = {
        "balanceOf",
        "ownerOf",
        "approve",
        "transferFrom",
        "safeTransferFrom",
        "setApprovalForAll",
        "getApproved",
        "isApprovedForAll"
    }

    # ERC-1155 functions
    erc1155_functions = {
        "safeBatchTransferFrom",
        "safeTransferFrom",
        "balanceOfBatch"
    }

    # ERC-2981 function
    erc2981_function = "royaltyInfo"

    # -------------------------------
    # Recursive AST Traversal
    # -------------------------------
    def traverse(node):
        if isinstance(node, dict):

            # Check function definitions
            if node.get("type") == "FunctionDefinition":
                name = node.get("name")

                if name in erc721_functions:
                    standards.add("ERC721")

                if name in erc1155_functions:
                    standards.add("ERC1155")

                if name == erc2981_function:
                    standards.add("ERC2981")

            # Traverse all children
            for value in node.values():
                traverse(value)

        elif isinstance(node, list):
            for item in node:
                traverse(item)

    # Start traversal
    traverse(ast)

    return standards
