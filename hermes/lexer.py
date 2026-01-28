"""
Hermes Lexer - Tokenizes Hermes source code
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional


class TokenType(Enum):
    # Keywords - Sangam skin (Vadivelu)
    SCHEME = auto()      # def
    ABANDON = auto()     # return
    FORTIFY = auto()     # class
    MYSELF = auto()      # self
    INITIALIZE = auto()  # __init__
    
    # Conditionals
    AAHAAN = auto()      # if
    CASCADE = auto()     # elif
    THATS_IT = auto()    # else
    
    # Loops
    ITERATE = auto()     # for
    WITHIN = auto()      # in
    REPEAT = auto()      # while
    COLLAPSE = auto()    # break
    SKIP = auto()        # continue
    
    # Error handling
    ATTEMPT = auto()     # try
    GRIEVE = auto()      # except
    VALIDATE = auto()    # finally
    ESCALATE = auto()    # raise
    
    # Values
    TRUTH = auto()       # True
    FALSEHOOD = auto()   # False
    NOTHING = auto()     # None
    
    # Logical/Comparison keywords
    SAME_AS = auto()        # ==
    DIFFERS_FROM = auto()   # !=
    GREATER_THAN = auto()   # >
    LESSER_THAN = auto()    # <
    AT_LEAST = auto()       # >=
    AT_MOST = auto()        # <=
    KINSHIP = auto()        # and
    ALTERNATE = auto()      # or
    NEGATE = auto()         # not
    
    # I/O
    ANNOUNCE = auto()    # print
    LISTEN = auto()      # input
    
    # Modules
    CONGREGATION = auto()  # import
    FROM = auto()          # from
    AS = auto()            # as
    
    # Advanced
    DESIRE = auto()      # lambda
    PRODUCE = auto()     # yield
    RECOGNIZE = auto()   # global
    CONTEXT = auto()     # with
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    DOUBLE_SLASH = auto()
    PERCENT = auto()
    DOUBLE_STAR = auto()
    
    ASSIGN = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    STAR_ASSIGN = auto()
    SLASH_ASSIGN = auto()
    
    EQ = auto()
    NE = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    COLON = auto()
    DOT = auto()
    ARROW = auto()
    AT = auto()
    
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    FSTRING = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Structure
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    COMMENT = auto()
    EOF = auto()


@dataclass(frozen=True, slots=True)
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class Lexer:
    KEYWORDS = {
        "scheme": TokenType.SCHEME,
        "abandon": TokenType.ABANDON,
        "fortify": TokenType.FORTIFY,
        "myself": TokenType.MYSELF,
        "initialize": TokenType.INITIALIZE,
        "aahaan": TokenType.AAHAAN,
        "cascade": TokenType.CASCADE,
        "thats_it": TokenType.THATS_IT,
        "iterate": TokenType.ITERATE,
        "within": TokenType.WITHIN,
        "repeat": TokenType.REPEAT,
        "collapse": TokenType.COLLAPSE,
        "skip": TokenType.SKIP,
        "attempt": TokenType.ATTEMPT,
        "grieve": TokenType.GRIEVE,
        "validate": TokenType.VALIDATE,
        "escalate": TokenType.ESCALATE,
        "truth": TokenType.TRUTH,
        "falsehood": TokenType.FALSEHOOD,
        "nothing": TokenType.NOTHING,
        "same_as": TokenType.SAME_AS,
        "differs_from": TokenType.DIFFERS_FROM,
        "greater_than": TokenType.GREATER_THAN,
        "lesser_than": TokenType.LESSER_THAN,
        "at_least": TokenType.AT_LEAST,
        "at_most": TokenType.AT_MOST,
        "kinship": TokenType.KINSHIP,
        "alternate": TokenType.ALTERNATE,
        "negate": TokenType.NEGATE,
        "announce": TokenType.ANNOUNCE,
        "listen": TokenType.LISTEN,
        "congregation": TokenType.CONGREGATION,
        "from": TokenType.FROM,
        "as": TokenType.AS,
        "desire": TokenType.DESIRE,
        "produce": TokenType.PRODUCE,
        "recognize": TokenType.RECOGNIZE,
        "context": TokenType.CONTEXT,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.indent_stack = [0]
        self.paren_depth = 0
    
    def peek(self, offset: int = 0) -> Optional[str]:
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        if self.pos < len(self.source):
            char = self.source[self.pos]
            self.pos += 1
            if char == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def add_token(self, type: TokenType, value: str, line: int = None, col: int = None):
        self.tokens.append(Token(type, value, line or self.line, col or self.column))
    
    def read_string(self, quote: str) -> str:
        result = []
        triple = self.peek() == quote and self.peek(1) == quote
        if triple:
            self.advance()
            self.advance()
        
        while True:
            char = self.peek()
            if char is None:
                raise SyntaxError(f"Unterminated string at line {self.line}")
            
            if triple:
                if char == quote and self.peek(1) == quote and self.peek(2) == quote:
                    self.advance()
                    self.advance()
                    self.advance()
                    break
            else:
                if char == quote:
                    self.advance()
                    break
                if char == "\n":
                    raise SyntaxError(f"Unterminated string at line {self.line}")
            
            if char == "\\":
                self.advance()
                escape = self.advance()
                escapes = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\"}
                if escape in escapes:
                    result.append(escapes[escape])
                elif escape == quote:
                    result.append(quote)
                else:
                    result.append("\\" + (escape or ""))
            else:
                result.append(self.advance())
        
        return "".join(result)
    
    def read_number(self) -> Token:
        start_col = self.column
        result = []
        is_float = False
        
        # Hex/binary/octal
        if self.peek() == "0" and self.peek(1) in ("x", "X", "b", "B", "o", "O"):
            result.append(self.advance())
            result.append(self.advance())
            valid = "0123456789abcdefABCDEF" if result[-1].lower() == "x" else "01234567" if result[-1].lower() == "o" else "01"
            while self.peek() and self.peek() in valid + "_":
                if self.peek() != "_":
                    result.append(self.advance())
                else:
                    self.advance()
            return Token(TokenType.INTEGER, "".join(result), self.line, start_col)
        
        # Regular number
        while self.peek() and (self.peek().isdigit() or self.peek() == "_"):
            if self.peek() != "_":
                result.append(self.advance())
            else:
                self.advance()
        
        # Decimal
        if self.peek() == "." and self.peek(1) and self.peek(1).isdigit():
            is_float = True
            result.append(self.advance())
            while self.peek() and (self.peek().isdigit() or self.peek() == "_"):
                if self.peek() != "_":
                    result.append(self.advance())
                else:
                    self.advance()
        
        # Exponent
        if self.peek() in ("e", "E"):
            is_float = True
            result.append(self.advance())
            if self.peek() in ("+", "-"):
                result.append(self.advance())
            while self.peek() and self.peek().isdigit():
                result.append(self.advance())
        
        return Token(TokenType.FLOAT if is_float else TokenType.INTEGER, "".join(result), self.line, start_col)
    
    def read_identifier(self) -> Token:
        start_col = self.column
        result = []
        while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
            result.append(self.advance())
        value = "".join(result)
        type = self.KEYWORDS.get(value, TokenType.IDENTIFIER)
        return Token(type, value, self.line, start_col)
    
    def tokenize(self) -> List[Token]:
        self.tokens = []
        self.indent_stack = [0]
        at_line_start = True
        
        while self.pos < len(self.source):
            # Handle indentation at line start
            if at_line_start and self.paren_depth == 0:
                indent = 0
                while self.peek() in (" ", "\t"):
                    indent += 4 if self.peek() == "\t" else 1
                    self.advance()
                
                if self.peek() == "\n":
                    self.advance()
                    continue
                if self.peek() == "#":
                    while self.peek() and self.peek() != "\n":
                        self.advance()
                    continue
                
                if indent > self.indent_stack[-1]:
                    self.indent_stack.append(indent)
                    self.add_token(TokenType.INDENT, "")
                else:
                    while indent < self.indent_stack[-1]:
                        self.indent_stack.pop()
                        self.add_token(TokenType.DEDENT, "")
                
                at_line_start = False
                continue
            
            char = self.peek()
            
            if char in (" ", "\t"):
                self.advance()
                continue
            
            if char == "\n":
                if self.paren_depth == 0:
                    self.add_token(TokenType.NEWLINE, "\\n")
                    at_line_start = True
                self.advance()
                continue
            
            if char == "#":
                start_col = self.column
                comment = []
                while self.peek() and self.peek() != "\n":
                    comment.append(self.advance())
                self.add_token(TokenType.COMMENT, "".join(comment), self.line, start_col)
                continue
            
            if char in ("\"", "'"):
                start_col = self.column
                quote = self.advance()
                is_fstring = self.tokens and self.tokens[-1].value == "f"
                if is_fstring:
                    self.tokens.pop()
                value = self.read_string(quote)
                self.add_token(TokenType.FSTRING if is_fstring else TokenType.STRING, value, self.line, start_col)
                continue
            
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            if char.isalpha() or char == "_":
                self.tokens.append(self.read_identifier())
                continue
            
            # Operators
            start_col = self.column
            ops = {
                "+": [("+", "=", TokenType.PLUS_ASSIGN), ("+", None, TokenType.PLUS)],
                "-": [("-", "=", TokenType.MINUS_ASSIGN), ("-", ">", TokenType.ARROW), ("-", None, TokenType.MINUS)],
                "*": [("*", "*", TokenType.DOUBLE_STAR), ("*", "=", TokenType.STAR_ASSIGN), ("*", None, TokenType.STAR)],
                "/": [("/", "/", TokenType.DOUBLE_SLASH), ("/", "=", TokenType.SLASH_ASSIGN), ("/", None, TokenType.SLASH)],
                "%": [("%", None, TokenType.PERCENT)],
                "=": [("=", "=", TokenType.EQ), ("=", None, TokenType.ASSIGN)],
                "!": [("!", "=", TokenType.NE)],
                "<": [("<", "=", TokenType.LE), ("<", None, TokenType.LT)],
                ">": [(">", "=", TokenType.GE), (">", None, TokenType.GT)],
                "(": [("(", None, TokenType.LPAREN)],
                ")": [(")", None, TokenType.RPAREN)],
                "[": [("[", None, TokenType.LBRACKET)],
                "]": [("]", None, TokenType.RBRACKET)],
                "{": [("{", None, TokenType.LBRACE)],
                "}": [("}", None, TokenType.RBRACE)],
                ",": [(",", None, TokenType.COMMA)],
                ":": [(":", None, TokenType.COLON)],
                ".": [(".", None, TokenType.DOT)],
                "@": [("@", None, TokenType.AT)],
            }
            
            if char in ops:
                self.advance()
                for _, next_char, token_type in ops[char]:
                    if next_char is None or self.peek() == next_char:
                        if next_char:
                            self.advance()
                        if char in "([{":
                            self.paren_depth += 1
                        elif char in ")]}":
                            self.paren_depth -= 1
                        self.add_token(token_type, char + (next_char or ""), self.line, start_col)
                        break
            else:
                raise SyntaxError(f"Unexpected character {char!r} at line {self.line}, column {self.column}")
        
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.add_token(TokenType.DEDENT, "")
        
        self.add_token(TokenType.EOF, "")
        return self.tokens
