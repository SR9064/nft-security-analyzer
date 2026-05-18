from solidity_parser import parser

def preprocess(source):
    # Convert modern Solidity syntax to parser-compatible syntax
    source = source.replace("{value:", ".value(")
    source = source.replace("}(", ")(")
    return source

def parse_contract(path):
    with open(path, 'r') as f:
        source = f.read()

    source = preprocess(source)  # ✅ only added line

    ast = parser.parse(source)
    return ast
