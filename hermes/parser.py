"""
Hermes Parser - Builds AST from tokens
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Union
from .lexer import Token, TokenType


# AST Node classes
@dataclass
class Node:
    line: int = 0
    column: int = 0


@dataclass
class Program(Node):
    statements: List["Statement"] = field(default_factory=list)


@dataclass
class FunctionDef(Node):
    name: str = ""
    params: List[str] = field(default_factory=list)
    body: List["Statement"] = field(default_factory=list)
    decorators: List["Expression"] = field(default_factory=list)


@dataclass
class ClassDef(Node):
    name: str = ""
    bases: List["Expression"] = field(default_factory=list)
    body: List["Statement"] = field(default_factory=list)


@dataclass
class If(Node):
    condition: "Expression" = None
    body: List["Statement"] = field(default_factory=list)
    elifs: List[tuple] = field(default_factory=list)  # [(condition, body), ...]
    else_body: List["Statement"] = field(default_factory=list)


@dataclass
class For(Node):
    target: str = ""
    iterable: "Expression" = None
    body: List["Statement"] = field(default_factory=list)


@dataclass
class While(Node):
    condition: "Expression" = None
    body: List["Statement"] = field(default_factory=list)


@dataclass
class TryExcept(Node):
    try_body: List["Statement"] = field(default_factory=list)
    handlers: List[tuple] = field(default_factory=list)  # [(type, name, body), ...]
    finally_body: List["Statement"] = field(default_factory=list)


@dataclass
class With(Node):
    items: List[tuple] = field(default_factory=list)  # [(context, target), ...]
    body: List["Statement"] = field(default_factory=list)


@dataclass
class Return(Node):
    value: Optional["Expression"] = None


@dataclass
class Yield(Node):
    value: Optional["Expression"] = None


@dataclass
class Raise(Node):
    exception: Optional["Expression"] = None


@dataclass
class Break(Node):
    pass


@dataclass
class Continue(Node):
    pass


@dataclass
class Global(Node):
    names: List[str] = field(default_factory=list)


@dataclass
class Import(Node):
    module: str = ""
    alias: Optional[str] = None


@dataclass
class ImportFrom(Node):
    module: str = ""
    names: List[tuple] = field(default_factory=list)  # [(name, alias), ...]


@dataclass
class ExprStmt(Node):
    expr: "Expression" = None


@dataclass
class Assign(Node):
    targets: List["Expression"] = field(default_factory=list)
    value: "Expression" = None


@dataclass
class AugAssign(Node):
    target: "Expression" = None
    op: str = ""
    value: "Expression" = None


# Expression nodes
@dataclass
class BinaryOp(Node):
    left: "Expression" = None
    op: str = ""
    right: "Expression" = None


@dataclass
class UnaryOp(Node):
    op: str = ""
    operand: "Expression" = None


@dataclass
class Compare(Node):
    left: "Expression" = None
    ops: List[str] = field(default_factory=list)
    comparators: List["Expression"] = field(default_factory=list)


@dataclass
class BoolOp(Node):
    op: str = ""  # "and" or "or"
    values: List["Expression"] = field(default_factory=list)


@dataclass
class Call(Node):
    func: "Expression" = None
    args: List["Expression"] = field(default_factory=list)
    kwargs: List[tuple] = field(default_factory=list)  # [(key, value), ...]


@dataclass
class Attribute(Node):
    value: "Expression" = None
    attr: str = ""


@dataclass
class Subscript(Node):
    value: "Expression" = None
    index: "Expression" = None


@dataclass
class Name(Node):
    id: str = ""


@dataclass
class Literal(Node):
    value: Any = None
    kind: str = ""  # "int", "float", "str", "bool", "none"


@dataclass
class List_(Node):
    elements: List["Expression"] = field(default_factory=list)


@dataclass
class Dict_(Node):
    keys: List["Expression"] = field(default_factory=list)
    values: List["Expression"] = field(default_factory=list)


@dataclass
class Lambda(Node):
    params: List[str] = field(default_factory=list)
    body: "Expression" = None


@dataclass
class IfExp(Node):
    test: "Expression" = None
    body: "Expression" = None
    orelse: "Expression" = None


Statement = Union[FunctionDef, ClassDef, If, For, While, TryExcept, With, Return, Yield, Raise, Break, Continue, Global, Import, ImportFrom, ExprStmt, Assign, AugAssign]
Expression = Union[BinaryOp, UnaryOp, Compare, BoolOp, Call, Attribute, Subscript, Name, Literal, List_, Dict_, Lambda, IfExp]


class Parser:
    """Recursive descent parser for Hermes"""
    
    def __init__(self):
        self.tokens: List[Token] = []
        self.pos = 0
    
    def current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]
    
    def peek(self, offset: int = 0) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def advance(self) -> Token:
        token = self.current()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def match(self, *types: TokenType) -> bool:
        return self.current().type in types
    
    def expect(self, type: TokenType) -> Token:
        if not self.match(type):
            raise SyntaxError(f"Expected {type.name}, got {self.current().type.name} at line {self.current().line}")
        return self.advance()
    
    def skip_newlines(self):
        while self.match(TokenType.NEWLINE, TokenType.COMMENT):
            self.advance()
    
    def parse(self, tokens: List[Token]) -> Program:
        self.tokens = tokens
        self.pos = 0
        
        statements = []
        self.skip_newlines()
        
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements=statements)
    
    def parse_statement(self) -> Optional[Statement]:
        self.skip_newlines()
        
        if self.match(TokenType.SCHEME):
            return self.parse_function_def()
        elif self.match(TokenType.FORTIFY):
            return self.parse_class_def()
        elif self.match(TokenType.AAHAAN):
            return self.parse_if()
        elif self.match(TokenType.ITERATE):
            return self.parse_for()
        elif self.match(TokenType.REPEAT):
            return self.parse_while()
        elif self.match(TokenType.ATTEMPT):
            return self.parse_try()
        elif self.match(TokenType.CONTEXT):
            return self.parse_with()
        elif self.match(TokenType.ABANDON):
            return self.parse_return()
        elif self.match(TokenType.PRODUCE):
            return self.parse_yield()
        elif self.match(TokenType.ESCALATE):
            return self.parse_raise()
        elif self.match(TokenType.COLLAPSE):
            self.advance()
            return Break(line=self.current().line)
        elif self.match(TokenType.SKIP):
            self.advance()
            return Continue(line=self.current().line)
        elif self.match(TokenType.RECOGNIZE):
            return self.parse_global()
        elif self.match(TokenType.CONGREGATION):
            return self.parse_import()
        elif self.match(TokenType.FROM):
            return self.parse_from_import()
        elif self.match(TokenType.AT):
            return self.parse_decorated()
        else:
            return self.parse_expr_or_assign()
    
    def parse_function_def(self) -> FunctionDef:
        token = self.expect(TokenType.SCHEME)
        # Allow INITIALIZE keyword as function name
        if self.match(TokenType.INITIALIZE):
            name = self.advance().value
        else:
            name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        params = []
        while not self.match(TokenType.RPAREN):
            # Allow MYSELF keyword as parameter  
            if self.match(TokenType.MYSELF):
                params.append(self.advance().value)
            else:
                params.append(self.expect(TokenType.IDENTIFIER).value)
            if self.match(TokenType.COMMA):
                self.advance()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.COLON)
        
        body = self.parse_block()
        return FunctionDef(name=name, params=params, body=body, line=token.line)
    
    def parse_class_def(self) -> ClassDef:
        token = self.expect(TokenType.FORTIFY)
        name = self.expect(TokenType.IDENTIFIER).value
        
        bases = []
        if self.match(TokenType.LPAREN):
            self.advance()
            while not self.match(TokenType.RPAREN):
                bases.append(self.parse_expression())
                if self.match(TokenType.COMMA):
                    self.advance()
            self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.COLON)
        body = self.parse_block()
        return ClassDef(name=name, bases=bases, body=body, line=token.line)
    
    def parse_if(self) -> If:
        token = self.expect(TokenType.AAHAAN)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        body = self.parse_block()
        
        elifs = []
        while self.match(TokenType.CASCADE):
            self.advance()
            elif_cond = self.parse_expression()
            self.expect(TokenType.COLON)
            elif_body = self.parse_block()
            elifs.append((elif_cond, elif_body))
        
        else_body = []
        if self.match(TokenType.THATS_IT):
            self.advance()
            self.expect(TokenType.COLON)
            else_body = self.parse_block()
        
        return If(condition=condition, body=body, elifs=elifs, else_body=else_body, line=token.line)
    
    def parse_for(self) -> For:
        token = self.expect(TokenType.ITERATE)
        target = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.WITHIN)
        iterable = self.parse_expression()
        self.expect(TokenType.COLON)
        body = self.parse_block()
        return For(target=target, iterable=iterable, body=body, line=token.line)
    
    def parse_while(self) -> While:
        token = self.expect(TokenType.REPEAT)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        body = self.parse_block()
        return While(condition=condition, body=body, line=token.line)
    
    def parse_try(self) -> TryExcept:
        token = self.expect(TokenType.ATTEMPT)
        self.expect(TokenType.COLON)
        try_body = self.parse_block()
        
        handlers = []
        while self.match(TokenType.GRIEVE):
            self.advance()
            exc_type = None
            exc_name = None
            if not self.match(TokenType.COLON):
                exc_type = self.expect(TokenType.IDENTIFIER).value
                if self.match(TokenType.AS):
                    self.advance()
                    exc_name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.COLON)
            handler_body = self.parse_block()
            handlers.append((exc_type, exc_name, handler_body))
        
        finally_body = []
        if self.match(TokenType.VALIDATE):
            self.advance()
            self.expect(TokenType.COLON)
            finally_body = self.parse_block()
        
        return TryExcept(try_body=try_body, handlers=handlers, finally_body=finally_body, line=token.line)
    
    def parse_with(self) -> With:
        token = self.expect(TokenType.CONTEXT)
        items = []
        
        context = self.parse_expression()
        target = None
        if self.match(TokenType.AS):
            self.advance()
            target = self.expect(TokenType.IDENTIFIER).value
        items.append((context, target))
        
        self.expect(TokenType.COLON)
        body = self.parse_block()
        return With(items=items, body=body, line=token.line)
    
    def parse_return(self) -> Return:
        token = self.expect(TokenType.ABANDON)
        value = None
        if not self.match(TokenType.NEWLINE, TokenType.EOF):
            value = self.parse_expression()
        return Return(value=value, line=token.line)
    
    def parse_yield(self) -> Yield:
        token = self.expect(TokenType.PRODUCE)
        value = None
        if not self.match(TokenType.NEWLINE, TokenType.EOF):
            value = self.parse_expression()
        return Yield(value=value, line=token.line)
    
    def parse_raise(self) -> Raise:
        token = self.expect(TokenType.ESCALATE)
        exception = None
        if not self.match(TokenType.NEWLINE, TokenType.EOF):
            exception = self.parse_expression()
        return Raise(exception=exception, line=token.line)
    
    def parse_global(self) -> Global:
        token = self.expect(TokenType.RECOGNIZE)
        names = [self.expect(TokenType.IDENTIFIER).value]
        while self.match(TokenType.COMMA):
            self.advance()
            names.append(self.expect(TokenType.IDENTIFIER).value)
        return Global(names=names, line=token.line)
    
    def parse_import(self) -> Import:
        token = self.expect(TokenType.CONGREGATION)
        module = self.expect(TokenType.IDENTIFIER).value
        alias = None
        if self.match(TokenType.AS):
            self.advance()
            alias = self.expect(TokenType.IDENTIFIER).value
        return Import(module=module, alias=alias, line=token.line)
    
    def parse_from_import(self) -> ImportFrom:
        token = self.expect(TokenType.FROM)
        module = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.CONGREGATION)
        
        names = []
        name = self.expect(TokenType.IDENTIFIER).value
        alias = None
        if self.match(TokenType.AS):
            self.advance()
            alias = self.expect(TokenType.IDENTIFIER).value
        names.append((name, alias))
        
        while self.match(TokenType.COMMA):
            self.advance()
            name = self.expect(TokenType.IDENTIFIER).value
            alias = None
            if self.match(TokenType.AS):
                self.advance()
                alias = self.expect(TokenType.IDENTIFIER).value
            names.append((name, alias))
        
        return ImportFrom(module=module, names=names, line=token.line)
    
    def parse_decorated(self) -> Statement:
        decorators = []
        while self.match(TokenType.AT):
            self.advance()
            decorators.append(self.parse_expression())
            self.skip_newlines()
        
        if self.match(TokenType.SCHEME):
            func = self.parse_function_def()
            func.decorators = decorators
            return func
        elif self.match(TokenType.FORTIFY):
            cls = self.parse_class_def()
            return cls
        else:
            raise SyntaxError(f"Expected function or class after decorator at line {self.current().line}")
    
    def parse_expr_or_assign(self) -> Statement:
        expr = self.parse_expression()
        
        if self.match(TokenType.ASSIGN):
            self.advance()
            value = self.parse_expression()
            return Assign(targets=[expr], value=value, line=expr.line)
        elif self.match(TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN, TokenType.STAR_ASSIGN, TokenType.SLASH_ASSIGN):
            op_token = self.advance()
            op = {TokenType.PLUS_ASSIGN: "+", TokenType.MINUS_ASSIGN: "-", TokenType.STAR_ASSIGN: "*", TokenType.SLASH_ASSIGN: "/"}[op_token.type]
            value = self.parse_expression()
            return AugAssign(target=expr, op=op, value=value, line=expr.line)
        else:
            return ExprStmt(expr=expr, line=expr.line)
    
    def parse_block(self) -> List[Statement]:
        self.skip_newlines()
        self.expect(TokenType.INDENT)
        
        statements = []
        while not self.match(TokenType.DEDENT, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        if self.match(TokenType.DEDENT):
            self.advance()
        
        return statements
    
    def parse_expression(self) -> Expression:
        return self.parse_or()
    
    def parse_or(self) -> Expression:
        left = self.parse_and()
        while self.match(TokenType.ALTERNATE):
            self.advance()
            right = self.parse_and()
            left = BoolOp(op="or", values=[left, right], line=left.line)
        return left
    
    def parse_and(self) -> Expression:
        left = self.parse_not()
        while self.match(TokenType.KINSHIP):
            self.advance()
            right = self.parse_not()
            left = BoolOp(op="and", values=[left, right], line=left.line)
        return left
    
    def parse_not(self) -> Expression:
        if self.match(TokenType.NEGATE):
            token = self.advance()
            return UnaryOp(op="not", operand=self.parse_not(), line=token.line)
        return self.parse_comparison()
    
    def parse_comparison(self) -> Expression:
        left = self.parse_add()
        
        ops = []
        comparators = []
        
        comp_tokens = {
            TokenType.SAME_AS: "==", TokenType.DIFFERS_FROM: "!=",
            TokenType.GREATER_THAN: ">", TokenType.LESSER_THAN: "<",
            TokenType.AT_LEAST: ">=", TokenType.AT_MOST: "<=",
            TokenType.EQ: "==", TokenType.NE: "!=",
            TokenType.LT: "<", TokenType.GT: ">",
            TokenType.LE: "<=", TokenType.GE: ">=",
            TokenType.WITHIN: "in",
        }
        
        while self.current().type in comp_tokens:
            ops.append(comp_tokens[self.advance().type])
            comparators.append(self.parse_add())
        
        if ops:
            return Compare(left=left, ops=ops, comparators=comparators, line=left.line)
        return left
    
    def parse_add(self) -> Expression:
        left = self.parse_mult()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = "+" if self.advance().type == TokenType.PLUS else "-"
            right = self.parse_mult()
            left = BinaryOp(left=left, op=op, right=right, line=left.line)
        return left
    
    def parse_mult(self) -> Expression:
        left = self.parse_unary()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.DOUBLE_SLASH, TokenType.PERCENT):
            op_map = {TokenType.STAR: "*", TokenType.SLASH: "/", TokenType.DOUBLE_SLASH: "//", TokenType.PERCENT: "%"}
            op = op_map[self.advance().type]
            right = self.parse_unary()
            left = BinaryOp(left=left, op=op, right=right, line=left.line)
        return left
    
    def parse_unary(self) -> Expression:
        if self.match(TokenType.MINUS):
            token = self.advance()
            return UnaryOp(op="-", operand=self.parse_unary(), line=token.line)
        return self.parse_power()
    
    def parse_power(self) -> Expression:
        left = self.parse_call()
        if self.match(TokenType.DOUBLE_STAR):
            self.advance()
            right = self.parse_unary()
            return BinaryOp(left=left, op="**", right=right, line=left.line)
        return left
    
    def parse_call(self) -> Expression:
        expr = self.parse_primary()
        
        while True:
            if self.match(TokenType.LPAREN):
                self.advance()
                args = []
                kwargs = []
                while not self.match(TokenType.RPAREN):
                    if self.match(TokenType.IDENTIFIER) and self.peek(1).type == TokenType.ASSIGN:
                        key = self.advance().value
                        self.advance()  # =
                        value = self.parse_expression()
                        kwargs.append((key, value))
                    else:
                        args.append(self.parse_expression())
                    if self.match(TokenType.COMMA):
                        self.advance()
                self.expect(TokenType.RPAREN)
                expr = Call(func=expr, args=args, kwargs=kwargs, line=expr.line)
            elif self.match(TokenType.DOT):
                self.advance()
                attr = self.expect(TokenType.IDENTIFIER).value
                expr = Attribute(value=expr, attr=attr, line=expr.line)
            elif self.match(TokenType.LBRACKET):
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = Subscript(value=expr, index=index, line=expr.line)
            else:
                break
        
        return expr
    
    def parse_primary(self) -> Expression:
        token = self.current()
        
        if self.match(TokenType.INTEGER):
            self.advance()
            return Literal(value=int(token.value, 0), kind="int", line=token.line)
        elif self.match(TokenType.FLOAT):
            self.advance()
            return Literal(value=float(token.value), kind="float", line=token.line)
        elif self.match(TokenType.STRING, TokenType.FSTRING):
            self.advance()
            return Literal(value=token.value, kind="str", line=token.line)
        elif self.match(TokenType.TRUTH):
            self.advance()
            return Literal(value=True, kind="bool", line=token.line)
        elif self.match(TokenType.FALSEHOOD):
            self.advance()
            return Literal(value=False, kind="bool", line=token.line)
        elif self.match(TokenType.NOTHING):
            self.advance()
            return Literal(value=None, kind="none", line=token.line)
        elif self.match(TokenType.IDENTIFIER, TokenType.MYSELF):
            self.advance()
            return Name(id=token.value, line=token.line)
        elif self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        elif self.match(TokenType.LBRACKET):
            return self.parse_list()
        elif self.match(TokenType.LBRACE):
            return self.parse_dict()
        elif self.match(TokenType.DESIRE):
            return self.parse_lambda()
        elif self.match(TokenType.ANNOUNCE):
            return self.parse_builtin_call("print")
        elif self.match(TokenType.LISTEN):
            return self.parse_builtin_call("input")
        else:
            raise SyntaxError(f"Unexpected token {token.type.name} at line {token.line}")
    
    def parse_list(self) -> List_:
        token = self.expect(TokenType.LBRACKET)
        elements = []
        while not self.match(TokenType.RBRACKET):
            elements.append(self.parse_expression())
            if self.match(TokenType.COMMA):
                self.advance()
        self.expect(TokenType.RBRACKET)
        return List_(elements=elements, line=token.line)
    
    def parse_dict(self) -> Dict_:
        token = self.expect(TokenType.LBRACE)
        keys = []
        values = []
        while not self.match(TokenType.RBRACE):
            key = self.parse_expression()
            self.expect(TokenType.COLON)
            value = self.parse_expression()
            keys.append(key)
            values.append(value)
            if self.match(TokenType.COMMA):
                self.advance()
        self.expect(TokenType.RBRACE)
        return Dict_(keys=keys, values=values, line=token.line)
    
    def parse_lambda(self) -> Lambda:
        token = self.expect(TokenType.DESIRE)
        params = []
        while not self.match(TokenType.COLON):
            params.append(self.expect(TokenType.IDENTIFIER).value)
            if self.match(TokenType.COMMA):
                self.advance()
        self.expect(TokenType.COLON)
        body = self.parse_expression()
        return Lambda(params=params, body=body, line=token.line)
    
    def parse_builtin_call(self, name: str) -> Call:
        token = self.advance()
        self.expect(TokenType.LPAREN)
        args = []
        while not self.match(TokenType.RPAREN):
            args.append(self.parse_expression())
            if self.match(TokenType.COMMA):
                self.advance()
        self.expect(TokenType.RPAREN)
        return Call(func=Name(id=name, line=token.line), args=args, kwargs=[], line=token.line)
