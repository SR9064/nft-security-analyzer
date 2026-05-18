from nftscanner.static_analysis.detectors.security.cross_contract_detector import (
    extract_contracts,
    detect_cross_reentrancy
)

from nftscanner.static_analysis.detectors.ownership.ownership_detector import (
    run_ownership_analysis
)

from nftscanner.static_analysis.detectors.nft.nft_property_detector import (
    run_nft_property_detection
)

from nftscanner.static_analysis.detectors.standards.compliance_detector import (
    run_compliance_checks
)

from nftscanner.static_analysis.detectors.nft_detector import (
    detect_nft_standard
)

# =========================================================
# SECURITY DETECTORS
# =========================================================
from nftscanner.static_analysis.detectors.security.tx_origin import (
    detect_tx_origin
)

from nftscanner.static_analysis.detectors.security.selfdestruct import (
    detect_selfdestruct
)

from nftscanner.static_analysis.detectors.security.delegatecall import (
    detect_delegatecall
)

from nftscanner.static_analysis.detectors.security.unchecked_call import (
    detect_unchecked_call
)

# =========================================================
# NFT DETECTORS
# =========================================================
from nftscanner.static_analysis.detectors.nft.unlimited_mint import (
    detect_unlimited_mint
)

from nftscanner.static_analysis.detectors.nft.metadata_mutable import (
    detect_mutable_metadata
)

from nftscanner.static_analysis.detectors.nft.royalty_abuse import (
    detect_royalty_abuse
)

from nftscanner.static_analysis.detectors.nft.hidden_mint import (
    detect_hidden_mint
)

from nftscanner.static_analysis.detectors.nft.approval_abuse import (
    detect_approval_abuse
)

from nftscanner.static_analysis.detectors.nft.unsafe_transfer import (
    detect_unsafe_transfer
)

# =========================================================
# OWNERSHIP DETECTORS
# =========================================================
from nftscanner.static_analysis.detectors.ownership.centralized_control import (
    detect_centralized_control
)


# =========================================================
# MAIN STATIC ANALYSIS ENGINE
# =========================================================
def run_static_analysis(ast, source_code):

    issues = []

    # -----------------------------------------------------
    # NFT STANDARD DETECTION
    # -----------------------------------------------------
    standards = detect_nft_standard(ast)

    # -----------------------------------------------------
    # OWNERSHIP ANALYSIS
    # -----------------------------------------------------
    issues += run_ownership_analysis(
        source_code
    )

    issues += detect_centralized_control(
        source_code
    )

    # -----------------------------------------------------
    # SECURITY DETECTORS
    # -----------------------------------------------------
    issues += detect_tx_origin(
        source_code
    )

    issues += detect_selfdestruct(
        source_code
    )

    issues += detect_delegatecall(
        source_code
    )

    issues += detect_unchecked_call(
        source_code
    )

    # -----------------------------------------------------
    # NFT PROPERTY ANALYSIS
    # -----------------------------------------------------
    issues += run_nft_property_detection(
        source_code
    )

    # -----------------------------------------------------
    # NFT DETECTORS
    # -----------------------------------------------------
    issues += detect_unlimited_mint(
        source_code
    )

    issues += detect_mutable_metadata(
        source_code
    )

    issues += detect_royalty_abuse(
        source_code
    )

    issues += detect_hidden_mint(
        source_code
    )

    issues += detect_approval_abuse(
        source_code
    )

    issues += detect_unsafe_transfer(
        source_code
    )

    # -----------------------------------------------------
    # CROSS CONTRACT ANALYSIS
    # -----------------------------------------------------
    contracts = extract_contracts(
        source_code
    )

    issues += detect_cross_reentrancy(
        contracts
    )

    # -----------------------------------------------------
    # COMPLIANCE CHECKS
    # -----------------------------------------------------
    issues += run_compliance_checks(
        ast,
        source_code,
        standards
    )

    return issues
