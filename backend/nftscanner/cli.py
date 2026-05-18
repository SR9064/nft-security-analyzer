import argparse
from nftscanner.main import run


def cli():
    parser = argparse.ArgumentParser(
        description="NFT Vulnerability Scanner"
    )

    parser.add_argument("contract", help="Path to Solidity contract")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    run(args.contract, args.verbose)


if __name__ == "__main__":
    cli()
