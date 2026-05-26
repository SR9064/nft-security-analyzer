import sys

from nftscanner.core.ast.parser import (
    parse_contract
)

from nftscanner.core.ir.ir_builder import (
    build_ir
)

from nftscanner.static_analysis.engine import (
    run_static_analysis
)

from nftscanner.reporting.reporter import (
    generate_report
)

from nftscanner.static_analysis.detectors.nft_detector import (
    detect_nft_standard
)

from nftscanner.symbolic_execution.executor.executor import (
    run_evm
)


# =====================================================
# MAIN ANALYZER
# =====================================================
def run(contract_path, verbose=False):

    # -------------------------------------------------
    # STEP 1 & 2
    # -------------------------------------------------
    if verbose:

        print("\n[STEP 1] START")

        print(
            "[STEP 2] Reading Solidity Smart Contract..."
        )

    # -------------------------------------------------
    # STEP 3 - AST
    # -------------------------------------------------
    ast = parse_contract(contract_path)

    # -------------------------------------------------
    # READ SOURCE
    # -------------------------------------------------
    with open(contract_path, "r") as f:

        source_code = f.read()

    if verbose:

        print(
            "[STEP 3] Generating Lightweight AST..."
        )

        print(
            "[STEP 3] Identifying NFT Standard..."
        )

    # -------------------------------------------------
    # NFT STANDARD DETECTION
    # -------------------------------------------------
    standards = list(
        detect_nft_standard(ast)
    )

    if not standards:

        standards = ["UNKNOWN"]

    if verbose:

        print(
            f"   → Detected Standards: {standards}"
        )

    # -------------------------------------------------
    # STEP 4 - STATIC ANALYSIS
    # -------------------------------------------------
    if verbose:

        print(
            "\n[STEP 4] NFT Static Analysis\n"
        )

    issues = run_static_analysis(
        ast,
        source_code
    )

    # -------------------------------------------------
    # STEP 6 - BUILD IR
    # -------------------------------------------------
    print(
        "\n[IR] Building Normalized IR..."
    )

    ir = build_ir(ast)

    print(
        "[IR] IR Generation Complete"
    )

    symbolic_vulns = []

    # -------------------------------------------------
    # STEP 7 - SYMBOLIC EXECUTION
    # -------------------------------------------------
    try:

        print(
            "\n[SYMBOLIC] Running Symbolic Execution..."
        )

        evm_result = run_evm(ir)

        # -------------------------------------------------
        # MERGE EVM VULNERABILITIES
        # -------------------------------------------------
        issues.extend(

            evm_result.get(
                "vulnerabilities",
                []
            )
        )

        # -------------------------------------------------
        # MERGE SYMBOLIC VULNERABILITIES
        # -------------------------------------------------
        issues.extend(

            evm_result.get(
                "symbolic_vulnerabilities",
                []
            )
        )

        symbolic_vulns = evm_result.get(
            "symbolic_vulnerabilities",
            []
        )

    except Exception as e:

        print(
            f"[SYMBOLIC ERROR] {e}"
        )

    # -------------------------------------------------
    # FINAL RISK MODEL
    # -------------------------------------------------
    risk = 0

    for issue in issues:

        severity = issue.get(
            "severity",
            ""
        ).upper()

        if severity == "CRITICAL":

            risk += 10

        elif severity == "HIGH":

            risk += 7

        elif severity == "MEDIUM":

            risk += 4

        elif severity == "LOW":

            risk += 1

    # -------------------------------------------------
    # FINAL RISK LEVEL
    # -------------------------------------------------
    if risk >= 30:

        level = "HIGH"

    elif risk >= 15:

        level = "MEDIUM"

    else:

        level = "LOW"

    if verbose:

        print(
            f"[FINAL RISK SCORE] {risk}"
        )

        print(
            f"[FINAL RISK LEVEL] {level}"
        )

    # -------------------------------------------------
    # STEP 8 - REPORT
    # -------------------------------------------------
    generate_report(
        issues,
        risk
    )

    print(
        f"Risk Level: {level}"
    )

    print(
        "✔ Manual review recommended for fixes."
    )

    # -------------------------------------------------
    # RETURN RESULTS
    # -------------------------------------------------
    return {

        "issues":
        issues,

        "symbolic_vulns":
        symbolic_vulns
    }


# =====================================================
# CLI ENTRY
# =====================================================
if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "Usage: python main.py <contract.sol>"
        )

        sys.exit(1)

    contract = sys.argv[1]

    verbose = (
        "--verbose" in sys.argv
        or "-v" in sys.argv
    )

    run(contract, verbose)
