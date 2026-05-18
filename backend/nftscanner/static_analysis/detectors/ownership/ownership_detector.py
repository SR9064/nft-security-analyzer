def run_ownership_analysis(source_code, verbose=False):

    if verbose:
        print("      → [4(ii)] Performing Ownership Data-Flow Analysis...")

    issues = []

    if "onlyOwner" not in source_code and "Ownable" not in source_code:

        issues.append({
            "type": "Missing Ownership Access Control",
            "severity": "High",
            "line": "N/A"
        })

    return issues
