def run_ownership_analysis(
    source_code,
    verbose=False
):

    if verbose:

        print(
            "      → [4(ii)] "
            "Performing Ownership "
            "Data-Flow Analysis..."
        )

    issues = []

    # =================================================
    # MISSING ACCESS CONTROL
    # =================================================
    if (

        "onlyOwner"
        not in source_code

        and

        "Ownable"
        not in source_code
    ):

        issues.append({

            "type":
                "Missing Ownership Access Control",

            "severity":
                "HIGH",

            "line":
                "N/A",

            "description":
                (
                    "Sensitive smart contract "
                    "functions can be executed "
                    "by any user because "
                    "ownership validation "
                    "is missing."
                ),

            "example":
                (
                    "function withdraw() public {\n"
                    "    payable(msg.sender)"
                    ".transfer(address(this).balance);\n"
                    "}"
                ),

            "recommendation":
                (
                    "Use OpenZeppelin Ownable "
                    "and apply onlyOwner "
                    "to sensitive functions "
                    "like mint(), withdraw(), "
                    "setURI(), or admin actions."
                )
        })

    return issues
