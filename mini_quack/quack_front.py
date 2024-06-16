"""Front end for Quack"""

from lark import Lark, Transformer
import argparse
import json
import sys


import logging

import quack_ast
import quack_ast_builder

from lark import tree as lark_tree
import pydot

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def cli():
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("source", type=argparse.FileType("r"),
                            nargs="?", default=sys.stdin)
    args = cli_parser.parse_args()
    return args


def cli():
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("source", type=argparse.FileType("r"),
                            nargs="?", default=sys.stdin)
    args = cli_parser.parse_args()
    return args


def method_table_walk(node: quack_ast.ASTNode, visit_state: dict):
        node.method_table_visit(visit_state)

def main():
    args = cli()
    quack_parser = Lark(open("qklib/quack_grammar.txt", "r"))
    text = "".join(args.source.readlines())
    tree = quack_parser.parse(text)
    print(tree.pretty("   "))
    #if args.ptree:
    lark_tree.pydot__tree_to_png(tree, "parse_tree.png")
    ast: quack_ast.ASTNode = quack_ast_builder.ASTBuilder().transform(tree)
    print(f"""
    /********
     * Reconstructed source from unparsing AST
     *********
     */
     {ast}
     
     /* **** End of reconstructed source *** */""")

    # Build symbol table, starting with the hard-coded json table
    # provided by Pranav.  We'll follow that structure for the rest
    builtins = open("qklib/builtin_methods.json")
    symtab = json.load(builtins)
    ast.walk(symtab, method_table_walk)
    print(f"\n\n\n****   Symbol table dump  ****")
    print(json.dumps(symtab,indent=4))


if __name__ == "__main__":
    main()







