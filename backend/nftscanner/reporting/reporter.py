from rich import print
from rich.panel import Panel
from rich.table import Table

from nftscanner.symbolic_execution.validation.smt_checker import (
    symbolic_check
)


# =========================================================
# FIX RECOMMENDATIONS
# =========================================================
def get_fix_recommendation(issue_type):

    fixes = {

        "Missing Ownership Access Control":
        "Add onlyOwner access control to sensitive NFT functions.",

        "Unauthorized Mint":
        "Restrict mint() using onlyOwner or role-based permissions.",

        "Unchecked External Call":
        "Validate return values from low-level external calls.",

        "Unlimited NFT Minting Risk":
        "Introduce immutable maxSupply validation before minting.",

        "Royalty Manipulation Risk":
        "Make royalty configuration immutable after deployment.",

        "Unsafe tx.origin Authentication":
        "Replace tx.origin with msg.sender authentication.",

        "Dangerous Delegatecall Usage":
        "Avoid delegatecall unless execution target is trusted.",

        "Dangerous Selfdestruct Usage":
        "Remove selfdestruct or restrict access using onlyOwner.",

        "Approval Misuse":
        "Validate ownership before approval operations.",

        "Hidden Owner Mint Capability":
        "Remove hidden privileged mint functionality.",

        "Approval For All Abuse Risk":
        "Restrict operator approvals and validate trusted operators.",

        "Unsafe ERC721 Transfer Usage":
        "Use safeTransferFrom() instead of transferFrom().",

        "Ownership Corruption":
        "Validate ownership updates and sanitize state transitions.",

        "Unauthorized Transfer":
        "Validate token ownership before transfers.",

        "Tainted Unauthorized Transfer":
        "Sanitize user-controlled transfer parameters."
    }

    return fixes.get(
        issue_type,
        "Manual security review recommended."
    )


# =========================================================
# REPORT GENERATOR
# =========================================================
def generate_report(issues, risk):

    print("\n")

    print(
        Panel.fit(
            "[bold cyan]NFT SECURITY ANALYSIS REPORT[/bold cyan]",
            border_style="cyan"
        )
    )

    # =====================================================
    # RISK LEVEL
    # =====================================================
    if risk >= 30:

        risk_level = "HIGH"
        risk_color = "red"

    elif risk >= 15:

        risk_level = "MEDIUM"
        risk_color = "yellow"

    else:

        risk_level = "LOW"
        risk_color = "green"

    print(
        f"\n[bold]Overall Risk Score:[/bold] "
        f"[{risk_color}]{risk}[/{risk_color}]"
    )

    print(
        f"[bold]Risk Level:[/bold] "
        f"[{risk_color}]{risk_level}[/{risk_color}]\n"
    )

    # =====================================================
    # NO ISSUES
    # =====================================================
    if not issues:

        print(
            "[green]✔ No vulnerabilities detected[/green]"
        )

        return

    # =====================================================
    # VULNERABILITY LOOP
    # =====================================================
    for idx, issue in enumerate(issues, start=1):

        issue_type = issue.get(
            "type",
            "Unknown Vulnerability"
        )

        severity = issue.get(
            "severity",
            "MEDIUM"
        ).upper()

        confidence = issue.get(
            "confidence",
            "MEDIUM"
        )

        line_info = issue.get(
            "line",
            "N/A"
        )

        # -------------------------------------------------
        # SEVERITY COLORS
        # -------------------------------------------------
        severity_color = {

            "CRITICAL": "red",
            "HIGH": "bright_red",
            "MEDIUM": "yellow",
            "LOW": "green"

        }.get(
            severity,
            "white"
        )

        # =================================================
        # ISSUE HEADER
        # =================================================
        print(
    f"[bold {severity_color}]"
    f"[{severity}] "
    f"{idx}. {issue_type}"
    f"[/]"
)

        print(
            f"   [bold]Line:[/bold] {line_info}"
        )

        print(
            f"   [bold]Confidence:[/bold] "
            f"{confidence}"
        )

        # =================================================
        # SMT VALIDATION
        # =================================================
        try:

            smt_result = symbolic_check(
                issue_type
            )

            if smt_result is True:

                print(
                    "   [green]"
                    "SMT Validation: "
                    "Exploit Confirmed"
                    "[/green]"
                )

            elif smt_result is False:

                print(
                    "   [yellow]"
                    "SMT Validation: "
                    "Exploit Not Reproducible"
                    "[/yellow]"
                )

        except Exception:

            pass

        # =================================================
        # ATTACK FLOW
        # =================================================
        if "attack_flow" in issue:

            print(
                "\n   [bold red]"
                "Attack Path:"
                "[/bold red]"
            )

            print(
                f"   {issue['attack_flow']}"
            )

        # =================================================
        # FIX RECOMMENDATION
        # =================================================
        recommendation = get_fix_recommendation(
            issue_type
        )

        print(
            "\n   [bold cyan]"
            "Recommendation:"
            "[/bold cyan]"
        )

        print(
            f"   {recommendation}"
        )

        # =================================================
        # ERC721 TEMPLATE
        # =================================================
        if "ERC-721 Missing Functions" in issue_type:

            print(
                "\n   [bold green]"
                "Minimal ERC-721 Template:"
                "[/bold green]"
            )

            print("""
function balanceOf(address owner) public view returns (uint256);

function ownerOf(uint256 tokenId)
    public
    view
    returns (address);

function transferFrom(
    address from,
    address to,
    uint256 tokenId
) public;

function safeTransferFrom(
    address from,
    address to,
    uint256 tokenId
) public;

function setApprovalForAll(
    address operator,
    bool approved
) public;

function getApproved(
    uint256 tokenId
) public view returns (address);

function isApprovedForAll(
    address owner,
    address operator
) public view returns (bool);

function supportsInterface(
    bytes4 interfaceId
) public view returns (bool);
""")

        print(
            "\n"
            + "-" * 60
            + "\n"
        )

    # =====================================================
    # FINAL SUMMARY
    # =====================================================
    print(
        Panel.fit(
            "[bold yellow]"
            "Manual Security Review Recommended"
            "[/bold yellow]",
            border_style="yellow"
        )
    )
