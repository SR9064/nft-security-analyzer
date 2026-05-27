# =========================================================
# NFT PROPERTY DETECTOR
# =========================================================

def extract_function_bodies(source_code):

    functions = {}
    lines = source_code.split("\n")

    current_func = None
    brace_count = 0

    for line in lines:

        stripped = line.strip()

        if stripped.startswith("function"):

            name = (
                stripped
                .split("function")[1]
                .split("(")[0]
                .strip()
            )

            current_func = name

            functions[current_func] = []

            brace_count = 0

        if current_func:

            functions[current_func].append(
                line
            )

            brace_count += line.count("{")

            brace_count -= line.count("}")

            if brace_count == 0:

                current_func = None

    return functions


# =========================================================
# MAIN NFT PROPERTY ANALYZER
# =========================================================
def run_nft_property_detection(
    source_code,
    verbose=False
):

    if verbose:

        print(
            "      → [4(iii)] Detecting NFT-Specific Vulnerabilities..."
        )

    issues = []

    seen_issues = set()

    function_bodies = extract_function_bodies(
        source_code
    )

    external_call_funcs = set()

    state_update_funcs = set()

    # -----------------------------------------------------
    # DETECT EXTERNAL CALL FUNCTIONS
    # -----------------------------------------------------
    for func, body in function_bodies.items():

        body_str = "\n".join(body)

        if (

            ".call(" in body_str

            or

            ".delegatecall(" in body_str

            or

            ".call{" in body_str
        ):

            external_call_funcs.add(
                func
            )

        if (

            "=" in body_str

            and

            (
                "balance" in body_str

                or

                "owner" in body_str
            )
        ):

            state_update_funcs.add(
                func
            )

    # -----------------------------------------------------
    # CROSS FUNCTION REENTRANCY
    # -----------------------------------------------------
    for func, body in function_bodies.items():

        body_str = "\n".join(body)

        if func in external_call_funcs:

            for target_func in state_update_funcs:

                if (

                    target_func in body_str

                    and

                    func != target_func
                ):

                    key = (
                        "Cross-Function Reentrancy Risk"
                    )

                    if (
                        key
                        not in seen_issues
                    ):

                        issues.append({

                            "type":
                                key,

                            "severity":
                                "HIGH",

                            "line":
                                "N/A",

                            "description":
                                (
                                    "An external contract call "
                                    "can trigger state-changing "
                                    "logic across multiple "
                                    "functions, enabling "
                                    "cross-function reentrancy."
                                ),

                            "example":
                                (
                                    "function withdraw() {\n"
                                    "    external.call(...);\n"
                                    "    balances[msg.sender] = 0;\n"
                                    "}"
                                ),

                            "recommendation":
                                (
                                    "Use ReentrancyGuard and "
                                    "follow checks-effects-"
                                    "interactions pattern."
                                )
                        })

                        seen_issues.add(
                            key
                        )

    # -----------------------------------------------------
    # ZERO ADDRESS VALIDATION
    # -----------------------------------------------------
    if "address(0)" not in source_code:

        issues.append({

            "type":
                "Missing Zero Address Validation",

            "severity":
                "MEDIUM",

            "line":
                "N/A",

            "description":
                (
                    "NFT minting or transfer "
                    "operations do not validate "
                    "against the zero address."
                ),

            "example":
                (
                    "_mint(address(0), tokenId);"
                ),

            "recommendation":
                (
                    "Validate all recipient "
                    "addresses using "
                    "require(to != address(0))."
                )
        })

    return issues
