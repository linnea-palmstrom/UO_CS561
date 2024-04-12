"""
Basic calculator
================

A simple example of a REPL calculator

This example shows how to write a basic calculator with variables.
"""
from lark import Lark, Transformer, v_args
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass


calc_grammar = """
    ?start: sum
          | NAME "=" sum    -> assign_var

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div

    ?atom: NUMBER           -> number
         | "-" atom         -> neg
         | NAME             -> var
         | "(" sum ")"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
"""

@v_args(inline=True)    # Affects the signatures of the methods
class EmitCode(Transformer):
    """Copying from CalculateTree except that we are not
    importing add, sub, etc from operator.
    """
    def __init__(self):
        log.debug("EmitCode constructor")

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def add(self, left, right):
        log.debug('sum "+" product   -> add')
        print("call Int:Plus")

    def sub(self, left, right):
        log.debug('sum "-" product   -> sub')
        print("call Int:Minus")

    def product(self, left):
        log.debug('?product: atom')

    def mul(self, left, right):
        log.debug('product "*" atom   -> mul')
        print("call Int:Times")

    def div(self, left, right):
        log.debug('product "/" atom   -> div')
        print("call Int:Div")

    def number(self, v):
        log.debug(f'number: {v}')
        print(f"const {v}")

    def neg(self, left):
        log.debug('"-" atom           -> neg')
        print("const 0")
        print("call Int:Minus")

    def var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            raise Exception("Variable not found: %s" % name)

@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg
    number = float

    def __init__(self):
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            raise Exception("Variable not found: %s" % name)


# calc_parser = Lark(calc_grammar, parser='lalr', transformer=CalculateTree())
calc_parser = Lark(calc_grammar, parser='lalr', transformer=EmitCode())
calc = calc_parser.parse


def main():
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(calc(s))


def test():
    print(calc("a = 1+2"))
    print(calc("1+a*-3"))


if __name__ == '__main__':
    # test()
    main()
