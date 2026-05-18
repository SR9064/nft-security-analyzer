#!/usr/bin/env python3
import os
import sys

if len(sys.argv) < 2:
    print("Usage: ./run_analyzer <contract.sol>")
    sys.exit(1)

contract = sys.argv[1]

os.system(f"nftscan {contract} -v")
