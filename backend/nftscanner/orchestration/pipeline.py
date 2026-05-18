from nftscanner.core.ast.parser import parse_contract

def run_pipeline(contract_path):
    ast = parse_contract(contract_path)
    return ast
