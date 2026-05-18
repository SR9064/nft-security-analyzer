# =========================================================
# HUMAN READABLE TRACE EXPLAINER
# =========================================================

def explain_instruction(stmt_type, stmt):

    # -----------------------------------------------------
    # FUNCTION ENTRY
    # -----------------------------------------------------
    if stmt_type == "FUNCTION":

        name = stmt.get(
            "name",
            "unknown"
        )

        # ---------------------------------------------
        # SKIP LOW VALUE ERC VIEW FUNCTIONS
        # ---------------------------------------------
        ignored_functions = [

            "constructor",
            "balanceOf",
            "balanceOfBatch",
            "ownerOf",
            "royaltyInfo",
            "supportsInterface",
            "name",
            "symbol",
            "tokenURI"

        ]

        if name in ignored_functions:

            return None

        return (
            f"Entered function: {name}()"
        )

    # -----------------------------------------------------
    # STORAGE WRITE
    # -----------------------------------------------------
    elif stmt_type == "SSTORE":

        slot = stmt.get(
            "slot",
            "unknown"
        )

        # ---------------------------------------------
        # SKIP UNKNOWN STORAGE
        # ---------------------------------------------
        if slot == "unknown":

            return None

        return (
            f"Contract storage updated "
            f"({slot})"
        )

    # -----------------------------------------------------
    # MEMORY WRITE
    # -----------------------------------------------------
    elif stmt_type == "MSTORE":

        # Too noisy for UI
        return None

    # -----------------------------------------------------
    # REQUIRE CHECK
    # -----------------------------------------------------
    elif stmt_type == "REQUIRE":

        condition = stmt.get(
            "condition",
            "unknown"
        )

        # ---------------------------------------------
        # CLEAN COMMON CONDITIONS
        # ---------------------------------------------
        replacements = {

            "msg.sender == owner":
            "Owner-only access validation",

            "msg.sender!=owner":
            "Unauthorized access blocked",

            "to != address(0)":
            "Zero-address protection check",

            "msg.value >":
            "Auction bid validation",

            "balance >=":
            "Balance verification",

            "signer != recovered":
            "Signature authentication check",

            "approved":
            "NFT approval verification",

            "locked == false":
            "Reentrancy lock verification",

            "supply <":
            "NFT supply limit validation"
        }

        for key, value in replacements.items():

            if key in condition:

                return value

        # ---------------------------------------------
        # FALLBACK
        # ---------------------------------------------
        if condition == "True":

            return None

        return (
            f"Security validation: {condition}"
        )

    # -----------------------------------------------------
    # EXTERNAL CALL
    # -----------------------------------------------------
    elif stmt_type == "CALL":

        target = stmt.get(
            "target",
            "external address"
        )

        if target == "UNKNOWN":

            return (
                "External contract interaction executed"
            )

        return (
            f"External contract call → {target}"
        )

    # -----------------------------------------------------
    # REENTRANCY
    # -----------------------------------------------------
    elif stmt_type == "REENTRY":

        target = stmt.get(
            "target",
            "unknown"
        )

        return (
            f"⚠ Reentrancy attempt detected "
            f"in {target}"
        )

    # -----------------------------------------------------
    # TOKEN TRANSFER
    # -----------------------------------------------------
    elif stmt_type == "TRANSFER":

        return (
            "NFT or ETH transfer executed"
        )

    # -----------------------------------------------------
    # OWNER CHANGE
    # -----------------------------------------------------
    elif stmt_type == "OWNER_CHANGE":

        return (
            "Ownership permissions modified"
        )

    # -----------------------------------------------------
    # FALLBACK
    # -----------------------------------------------------
    return None
