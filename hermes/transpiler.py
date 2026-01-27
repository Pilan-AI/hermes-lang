"""
Hermes Transpiler - Converts AST to Python code
"""

from typing import List
from .parser import (
    Node, Program, FunctionDef, ClassDef, If, For, While, TryExcept, With,
    Return, Yield, Raise, Break, Continue, Global, Import, ImportFrom,
    ExprStmt, Assign, AugAssign, BinaryOp, UnaryOp, Compare, BoolOp,
    Call, Attribute, Subscript, Name, Literal, List_, Dict_, Lambda, IfExp
)


class Transpiler:
    """Transpiles Hermes AST to Python source code"""
    
    # Hermes identifier mappings to Python
    ID_MAP = {
        "myself": "self",
        "initialize": "__init__",
        "truth": "True",
        "falsehood": "False",
        "nothing": "None",
    }
    
    def __init__(self):
        self.indent = 0
    
    def transpile(self, node: Node) -> str:
        if isinstance(node, Program):
            return self.visit_program(node)
        return self.visit(node)
    
    def ind(self) -> str:
        return "    " * self.indent
    
    def visit(self, node: Node) -> str:
        method = f"visit_{type(node).__name__.lower().rstrip('_')}"
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: Node) -> str:
        raise NotImplementedError(f"No visitor for {type(node).__name__}")
    
    def visit_program(self, node: Program) -> str:
        lines = []
        for stmt in node.statements:
            lines.append(self.visit(stmt))
        return "\n".join(lines)
    
    def visit_functiondef(self, node: FunctionDef) -> str:
        lines = []
        for dec in node.decorators:
            lines.append(f"{self.ind()}@{self.visit(dec)}")
        
        # Map parameter names
        params = [self.ID_MAP.get(p, p) for p in node.params]
        lines.append(f"{self.ind()}def {self.ID_MAP.get(node.name, node.name)}({', '.join(params)}):")
        
        self.indent += 1
        if not node.body:
            lines.append(f"{self.ind()}pass")
        else:
            for stmt in node.body:
                lines.append(self.visit(stmt))
        self.indent -= 1
        
        return "\n".join(lines)
    
    def visit_classdef(self, node: ClassDef) -> str:
        lines = []
        bases = ", ".join(self.visit(b) for b in node.bases) if node.bases else ""
        if bases:
            lines.append(f"{self.ind()}class {node.name}({bases}):")
        else:
            lines.append(f"{self.ind()}class {node.name}:")
        
        self.indent += 1
        if not node.body:
            lines.append(f"{self.ind()}pass")
        else:
            for stmt in node.body:
                lines.append(self.visit(stmt))
        self.indent -= 1
        
        return "\n".join(lines)
    
    def visit_if(self, node: If) -> str:
        lines = []
        lines.append(f"{self.ind()}if {self.visit(node.condition)}:")
        
        self.indent += 1
        for stmt in node.body:
            lines.append(self.visit(stmt))
        self.indent -= 1
        
        for cond, body in node.elifs:
            lines.append(f"{self.ind()}elif {self.visit(cond)}:")
            self.indent += 1
            for stmt in body:
                lines.append(self.visit(stmt))
            self.indent -= 1
        
        if node.else_body:
            lines.append(f"{self.ind()}else:")
            self.indent += 1
            for stmt in node.else_body:
                lines.append(self.visit(stmt))
            self.indent -= 1
        
        return "\n".join(lines)
    
    def visit_for(self, node: For) -> str:
        lines = []
        lines.append(f"{self.ind()}for {node.target} in {self.visit(node.iterable)}:")
        
        self.indent += 1
        for stmt in node.body:
            lines.append(self.visit(stmt))
        self.indent -= 1
        
        return "\n".join(lines)
    
    def visit_while(self, node: While) -> str:
        lines = []
        lines.append(f"{self.ind()}while {self.visit(node.condition)}:")
        
        self.indent += 1
        for stmt in node.body:
            lines.append(self.visit(stmt))
        self.indent -= 1
        
        return "\n".join(lines)
    
    def visit_tryexcept(self, node: TryExcept) -> str:
        lines = []
        lines.append(f"{self.ind()}try:")
        
        self.indent += 1
        for stmt in node.try_body:
            lines.append(self.visit(stmt))
        self.indent -= 1
        
        for exc_type, exc_name, handler_body in node.handlers:
            if exc_type and exc_name:
                lines.append(f"{self.ind()}except {exc_type} as {exc_name}:")
            elif exc_type:
                lines.append(f"{self.ind()}except {exc_type}:")
            else:
                lines.append(f"{self.ind()}except:")
            
            self.indent += 1
            for stmt in handler_body:
                lines.append(self.visit(stmt))
            self.indent -= 1
        
        if node.finally_body:
            lines.append(f"{self.ind()}finally:")
            self.indent += 1
            for stmt in node.finally_body:
                lines.append(self.visit(stmt))
            self.indent -= 1
        
        return "\n".join(lines)
    
    def visit_with(self, node: With) -> str:
        lines = []
        items = []
        for ctx, target in node.items:
            if target:
                items.append(f"{self.visit(ctx)} as {target}")
            else:
                items.append(self.visit(ctx))
        
        lines.append(f"{self.ind()}with {', '.join(items)}:")
        
        self.indent += 1
        for stmt in node.body:
            lines.append(self.visit(stmt))
        self.indent -= 1
        
        return "\n".join(lines)
    
    def visit_return(self, node: Return) -> str:
        if node.value:
            return f"{self.ind()}return {self.visit(node.value)}"
        return f"{self.ind()}return"
    
    def visit_yield(self, node: Yield) -> str:
        if node.value:
            return f"{self.ind()}yield {self.visit(node.value)}"
        return f"{self.ind()}yield"
    
    def visit_raise(self, node: Raise) -> str:
        if node.exception:
            return f"{self.ind()}raise {self.visit(node.exception)}"
        return f"{self.ind()}raise"
    
    def visit_break(self, node: Break) -> str:
        return f"{self.ind()}break"
    
    def visit_continue(self, node: Continue) -> str:
        return f"{self.ind()}continue"
    
    def visit_global(self, node: Global) -> str:
        return f"{self.ind()}global {', '.join(node.names)}"
    
    def visit_import(self, node: Import) -> str:
        if node.alias:
            return f"{self.ind()}import {node.module} as {node.alias}"
        return f"{self.ind()}import {node.module}"
    
    def visit_importfrom(self, node: ImportFrom) -> str:
        names = []
        for name, alias in node.names:
            if alias:
                names.append(f"{name} as {alias}")
            else:
                names.append(name)
        return f"{self.ind()}from {node.module} import {', '.join(names)}"
    
    def visit_exprstmt(self, node: ExprStmt) -> str:
        return f"{self.ind()}{self.visit(node.expr)}"
    
    def visit_assign(self, node: Assign) -> str:
        targets = " = ".join(self.visit(t) for t in node.targets)
        return f"{self.ind()}{targets} = {self.visit(node.value)}"
    
    def visit_augassign(self, node: AugAssign) -> str:
        return f"{self.ind()}{self.visit(node.target)} {node.op}= {self.visit(node.value)}"
    
    def visit_binaryop(self, node: BinaryOp) -> str:
        return f"({self.visit(node.left)} {node.op} {self.visit(node.right)})"
    
    def visit_unaryop(self, node: UnaryOp) -> str:
        if node.op == "not":
            return f"(not {self.visit(node.operand)})"
        return f"({node.op}{self.visit(node.operand)})"
    
    def visit_compare(self, node: Compare) -> str:
        parts = [self.visit(node.left)]
        for op, comp in zip(node.ops, node.comparators):
            parts.append(op)
            parts.append(self.visit(comp))
        return f"({' '.join(parts)})"
    
    def visit_boolop(self, node: BoolOp) -> str:
        values = f" {node.op} ".join(self.visit(v) for v in node.values)
        return f"({values})"
    
    def visit_call(self, node: Call) -> str:
        args = [self.visit(a) for a in node.args]
        for key, value in node.kwargs:
            args.append(f"{key}={self.visit(value)}")
        func_name = self.visit(node.func)
        return f"{func_name}({', '.join(args)})"
    
    def visit_attribute(self, node: Attribute) -> str:
        return f"{self.visit(node.value)}.{self.ID_MAP.get(node.attr, node.attr)}"
    
    def visit_subscript(self, node: Subscript) -> str:
        return f"{self.visit(node.value)}[{self.visit(node.index)}]"
    
    def visit_name(self, node: Name) -> str:
        return self.ID_MAP.get(node.id, node.id)
    
    def visit_literal(self, node: Literal) -> str:
        if node.kind == "str":
            escaped = node.value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
            return f'"{escaped}"'
        elif node.kind == "bool":
            return "True" if node.value else "False"
        elif node.kind == "none":
            return "None"
        return repr(node.value)
    
    def visit_list(self, node: List_) -> str:
        elements = ", ".join(self.visit(e) for e in node.elements)
        return f"[{elements}]"
    
    def visit_dict(self, node: Dict_) -> str:
        items = ", ".join(f"{self.visit(k)}: {self.visit(v)}" for k, v in zip(node.keys, node.values))
        return f"{{{items}}}"
    
    def visit_lambda(self, node: Lambda) -> str:
        params = ", ".join(self.ID_MAP.get(p, p) for p in node.params)
        return f"(lambda {params}: {self.visit(node.body)})"
    
    def visit_ifexp(self, node: IfExp) -> str:
        return f"({self.visit(node.body)} if {self.visit(node.test)} else {self.visit(node.orelse)})"
