"""AST classes for Quack"""

from lark import Lark, Transformer
import argparse
import json
import sys

from typing import List,  Callable

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

LB = "{"
RB = "}"

def ignore(node: "ASTNode", visit_state):
    log.debug(f"No visitor action at {node.__class__.__name__} node")
    return

def flatten(m: list):
    """Flatten nested lists into a single level of list"""
    flat = []
    for item in m:
        if isinstance(item, list):
            flat += flatten(item)
        else:
            flat.append(item)
    return flat


class ASTNode:
    """Abstract base class"""
    def __init__(self):
        self.children = []    # Internal nodes should set this to list of child nodes

    # Visitor-like functionality for walking over the AST. Define default methods in ASTNode
    # and specific overrides in node types in which the visitor should do something
    def walk(self, visit_state, pre_visit: Callable =ignore, post_visit: Callable=ignore):
        pre_visit(self, visit_state)
        for child in flatten(self.children):
            log.debug(f"Visiting ASTNode of class {child.__class__.__name__}")
            child.walk(visit_state, pre_visit, post_visit)
        post_visit(self, visit_state)

    # Example walk to gather method signatures
    def method_table_visit(self, visit_state: dict):
        ignore(self, visit_state)

    def r_eval(self) -> List[str]:
        """Evaluate for value"""
        raise NotImplementedError(f"r_eval not implemented for node type {self.__class__.__name__}")

    def c_eval(self, true_branch: str, false_branch: str) -> List[str]:
        raise NotImplementedError(f"c_eval not implemented for node type {self.__class__.__name__}")


class ProgramNode(ASTNode):
    def __init__(self, classes: List[ASTNode], main_block: ASTNode):
        self.classes = classes
        main_class = ClassNode("$Main", [], "Obj", [], main_block)
        self.classes.append(main_class)
        self.children = self.classes

    def __str__(self) -> str:
        return "\n".join([str(c) for c in self.classes])


class ClassNode(ASTNode):
    def __init__(self, name: str, formals: List[ASTNode],
                 super_class: str,
                 methods: List[ASTNode],
                 block: ASTNode):
        self.name = name
        self.super_class = super_class
        self.methods = methods
        self.constructor = MethodNode("$constructor", formals, name, block)
        self.children = methods +  [self.constructor]

    def __str__(self):
        formals_str = ", ".join([str(fm) for fm in self.constructor.formals])
        methods_str = "\n".join([f"{method}\n" for method in self.methods])
        return f"""
        class {self.name}({formals_str}){LB}
        {methods_str}
        /* statements as a constructor */
        {self.constructor}
        {RB} /* end class {self.name} */
        """

    # Example walk to gather method signatures
    def method_table_visit(self, visit_state: dict):
        """Create class entry in symbol table (as a preorder visit)"""
        if self.name in visit_state:
            raise Exception(f"Shadowing class {self.name} is not permitted")
        visit_state["current_class"] = self.name
        visit_state[self.name] = {
            "super": self.super_class,
            "fields": [],
            "methods": {}
        }



class MethodNode(ASTNode):
    def __init__(self, name: str, formals: List[ASTNode],
                 returns: str, body: ASTNode):
        self.name = name
        self.formals = formals
        self.returns = returns
        self.body = body
        self.children = [formals, body]

    def __str__(self):
        formals_str = ", ".join([str(fm) for fm in self.formals])
        return f"""
        /* method */ 
        def {self.name}({formals_str}): {self.returns} {LB}
        {self.body}
        {RB} /* End of method {self.name} */ 
        """

    # Add this method to the symbol table
    def method_table_visit(self, visit_state: dict):
        clazz = visit_state["current_class"]
        if self.name in visit_state[clazz]["methods"]:
            raise Exception(f"Redeclaration of method {self.name} not permitted")
        params = [formal.var_type for formal in self.formals]
        visit_state[clazz]["methods"][self.name] = { "params": params, "ret": self.returns }


class FormalNode(ASTNode):
    def __init__(self, var_name: str, var_type: str):
        self.var_name = var_name
        self.var_type = var_type
        self.children = []

    def __str__(self):
        return f"{self.var_name}: {self.var_type}"


class BlockNode(ASTNode):
    def __init__(self, stmts: List[ASTNode]):
        self.stmts = stmts
        self.children = stmts

    def __str__(self):
        return "".join([str(stmt) + ";\n" for stmt in self.stmts])


class AssignmentNode(ASTNode):
    """Placeholder ... not defined in grammar yet"""
    def __init__(self, blah: str):
        self.blah = blah
        self.children = []

    def __str__(self):
        return  self.blah

class ExprNode(ASTNode):
    """Just identifiers in this stub"""
    def __init__(self, e):
        self.e = e
        self.children = [e]

    def __str__(self):
        return str(self.e)

class VariableRefNode(ASTNode):
    """Reference to a variable in an expression.
    This will typically evaluate to a 'load' operation.
    """
    def __init__(self, name: str):
        assert isinstance(name, str)
        self.name = name
        self.children = []

    def __str__(self):
        return self.name

class IfStmtNode(ASTNode):
    def __init__(self,
                 cond: ASTNode,
                 thenpart: ASTNode,
                 elsepart: ASTNode):
        self.cond = cond
        self.thenpart = thenpart
        self.elsepart = elsepart
        self.children = [cond, thenpart, elsepart]

    def __str__(self):
        return f"""if {self.cond} {LB}\n
                {self.thenpart}
             {RB} else {LB}
                {self.elsepart} {LB}
            {RB}
            """

class CondNode(ASTNode):
    """Boolean condition. It can evaluate to jumps,
    but in this grammar it's just a placeholder.
    """
    def __init__(self, cond: str):
        self.cond = cond

    def __str__(self):
        return f"{self.cond}"
