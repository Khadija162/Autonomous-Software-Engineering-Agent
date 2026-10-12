"""Tree-sitter-powered Python syntax checks for proposed patches."""
import tree_sitter_python
from tree_sitter import Language, Parser


def parse_python(source: str) -> dict:
    parser = Parser(Language(tree_sitter_python.language()))
    tree = parser.parse(source.encode())
    return {"valid": not tree.root_node.has_error,
            "root_node": tree.root_node.type, "bytes": len(source.encode())}
