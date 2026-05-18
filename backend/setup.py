from setuptools import setup, find_packages

setup(
    name="nftscanner",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "nftscan=nftscanner.cli:cli"
        ]
    },
)
