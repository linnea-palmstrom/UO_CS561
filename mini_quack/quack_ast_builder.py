"""AST builder for Quack"""

from lark import Lark, Transformer
import argparse
import json
import sys

from typing import List,  Callable

import quack_ast

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class ASTBuilder(Transformer):
    """Translate Lark tree into my AST structure"""

    def program(self, e):
        log.debug("->program")
        classes, main_block = e
        return quack_ast.ProgramNode(classes, main_block)

    def classes(self, e):
        return e

    def clazz(self, e):
        log.debug("->clazz")
        name, formals, super, methods, constructor = e
        return quack_ast.ClassNode(name, formals, super, methods, constructor)

    def methods(self, e):
        return e

    def method(self, e):
        log.debug("->method")
        name, formals, returns, body = e
        return quack_ast.MethodNode(name, formals, returns, body)

    def returns(self, e):
        if not e:
            return "Nothing"
        return e

    def formals(self, e):
        if e[0] is None:
            return []
        return e

    def formal(self, e):
        log.debug("->formal")
        var_name, var_type = e
        return quack_ast.FormalNode(var_name, var_type)

    #def expr(self, e):
        #log.debug("->expr")
        #return quack_ast.ExprNode(e[0])
    
    def sum(self, e):
        log.debug("->sum")
        return quack_ast.SumNode(e[0])

    def product(self, e):
        log.debug("->product")
        return quack_ast.ProductNode(e[0])

    def ident(self, e):
        """A terminal symbol """
        log.debug("->ident")
        return e[0]

    def int_const(self, e):
        """A terminal symbol """
        log.debug("->int_const")
        return e[0]

    def str_const(self, e):
        """A terminal symbol """
        log.debug("->str_const")
        return e[0]

    def name(self, e):
        """A terminal symbol """
        log.debug("->name")
        return e[0]

    def variable_ref(self, e):
        """A reference to a variable"""
        log.debug("->variable_ref")
        return quack_ast.VariableRefNode(e[0])

    def block(self, e) -> quack_ast.ASTNode:
        log.debug("->block")
        stmts = e
        return quack_ast.BlockNode(stmts)

    def assignment(self, e) -> quack_ast.ASTNode:
        log.debug("->assignment")
        # Structure of e is [Token('BLAH','blah')]
        #blah = str(e[0])
        lhs, t, rhs = e
        #return quack_ast.AssignmentNode(blah)
        assert isinstance(lhs, str)
        return quack_ast.AssignmentNode(lhs, t, rhs)


    def ifstmt(self, e) -> quack_ast.ASTNode:
        log.debug("->ifstmt")
        cond, thenpart, elsepart = e
        return quack_ast.IfStmtNode(cond, thenpart, elsepart)

    def otherwise(self, e) -> quack_ast.ASTNode:
        log.debug("->otherwise")
        return e

    def elseblock(self, e) -> quack_ast.ASTNode:
        log.debug("->elseblock")
        return e[0]  # Unwrap one level of block

    def cond(self, e) -> quack_ast.ASTNode:
        log.debug("->cond")
        return e

    def value(self, e):
        log.debug("->value")
        child = e[0]
        return quack_ast.ValueNode(child)
