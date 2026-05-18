import os
import difflib
import re


def apply_fixes(source_code, issues):

    fixed_code = source_code

    # ----------------------------------------
    # Fix Unauthorized Mint (ONLY OWNER)
    # ----------------------------------------
    if any(issue["type"] == "Unauthorized Mint" for issue in issues):

        if "modifier onlyOwner" not in fixed_code:
            owner_modifier = """
address public owner;

constructor() {
    owner = msg.sender;
}

modifier onlyOwner() {
    require(msg.sender == owner, "Not owner");
    _;
}
"""
            fixed_code = owner_modifier + "\n" + fixed_code

        fixed_code = re.sub(
            r'function\s+mint\s*\((.*?)\)\s*public\s*{',
            r'function mint(\1) public onlyOwner {',
            fixed_code
        )

    # ----------------------------------------
    # Fix Approval Misuse (TOKEN OWNER CHECK)
    # ----------------------------------------
    if any(issue["type"] == "Approval Misuse" for issue in issues):

        lines = fixed_code.split("\n")
        new_lines = []

        for line in lines:
            new_lines.append(line)

            if line.strip().startswith("function approve"):
                new_lines.append(
                    '        require(msg.sender == ownerOf(tokenId), "Not token owner");'
                )

        fixed_code = "\n".join(new_lines)

    return fixed_code


def write_fixed_contract(original_code, fixed_code):

    os.makedirs("output", exist_ok=True)

    with open("output/fixed_contract.sol", "w") as f:
        f.write(fixed_code)

    print("\n✔ Fixed contract written to output/fixed_contract.sol")

    print("\nDiff (Original vs Fixed):\n")

    diff = difflib.unified_diff(
        original_code.splitlines(),
        fixed_code.splitlines(),
        fromfile="original.sol",
        tofile="fixed_contract.sol",
        lineterm=""
    )

    for line in diff:
        print(line)
