from setuptools import setup

setup(
    name="nftscanner",
    version="1.0",
    packages=["nftscanner"],   # force include
    py_modules=["main"],       # 🔥 IMPORTANT (this was missing)
    entry_points={
        "console_scripts": [
            "nftscan=nftscanner.cli:cli"
        ]
    },
)
