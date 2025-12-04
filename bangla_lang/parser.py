"""Parser skeleton for BPL (Bangla Programming Language).

This module provides a simple recursive-descent parser that will be extended
as the AST and grammar are implemented. For now it accepts a token stream and
produces a `Program` node placeholder.
"""
from typing import List, Optional

from .tokens import Token, INDENT, DEDENT, NEWLINE, EOF, IDENT, NUMBER, STRING, KEYWORD, OP, DELIM, BOOL, NIL
from .ast import Program, ExprStmt, Assign, Identifier, Literal, BinaryOp, UnaryOp, Call, FunctionDef, If, While, Return
from .errors import ParseError


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def accept(self, *types) -> Optional[Token]:
        if self.peek().type in types:
            return self.advance()
        return None

    def expect(self, typ, value=None) -> Token:
        tok = self.peek()
        if tok.type != typ:
            raise ParseError(f"সিনট্যাক্স ত্রুটি: প্রত্যাশিত {typ} কিন্তু পাওয়া যায় {tok.type} লাইন {tok.lineno}")
        if value is not None and tok.value != value:
            raise ParseError(f"সিনট্যাক্স ত্রুটি: প্রত্যাশিত '{value}' কিন্তু পাওয়া যায় '{tok.value}' লাইন {tok.lineno}")
        return self.advance()

    def parse(self) -> Program:
        stmts = []
        while self.peek().type != EOF:
            if self.peek().type == NEWLINE:
                self.advance()
                continue
            stmts.append(self.parse_statement())
        return Program(body=stmts)

    # Statements
    def parse_statement(self):
        tok = self.peek()
        if tok.type == KEYWORD and tok.value == "ফাংশন":
            return self.parse_function_def()
        if tok.type == KEYWORD and tok.value == "যদি":
            return self.parse_if()
        if tok.type == KEYWORD and tok.value == "যখন":
            return self.parse_while()
        if tok.type == KEYWORD and tok.value == "ফলাফল":
            return self.parse_return()
        # simple statement
        node = self.parse_simple_statement()
        # expect NEWLINE
        if self.peek().type == NEWLINE:
            self.advance()
        return node

    def parse_simple_statement(self):
        expr = self.parse_expression()
        # assignment
        if self.peek().type == OP and self.peek().value == "=":
            if not isinstance(expr, Identifier):
                raise ParseError(f"সিনট্যাক্স ত্রুটি: বাম পাশে একটি নাম থাকতে হবে লাইন {self.peek().lineno}")
            self.advance()  # consume '='
            value = self.parse_expression()
            return Assign(target=expr, value=value, lineno=expr.lineno, col=expr.col)
        return ExprStmt(value=expr, lineno=expr.lineno, col=expr.col)

    def parse_function_def(self):
        kw = self.expect(KEYWORD)
        name_tok = self.expect(IDENT)
        name = name_tok.value
        self.expect(DELIM, "(")
        params = []
        if self.peek().type != DELIM or self.peek().value != ")":
            while True:
                p = self.expect(IDENT)
                params.append(p.value)
                if self.peek().type == DELIM and self.peek().value == ",":
                    self.advance()
                    continue
                break
        self.expect(DELIM, ")")
        self.expect(DELIM, ":")
        self.expect(NEWLINE)
        self.expect(INDENT)
        body = []
        while self.peek().type != DEDENT:
            if self.peek().type == NEWLINE:
                self.advance()
                continue
            body.append(self.parse_statement())
        self.expect(DEDENT)
        return FunctionDef(name=name, params=params, body=body, lineno=kw.lineno, col=kw.col)

    def parse_if(self):
        kw = self.expect(KEYWORD)
        test = self.parse_expression()
        self.expect(DELIM, ":")
        self.expect(NEWLINE)
        self.expect(INDENT)
        body = []
        while self.peek().type != DEDENT:
            if self.peek().type == NEWLINE:
                self.advance()
                continue
            body.append(self.parse_statement())
        self.expect(DEDENT)
        orelse = []
        if self.peek().type == KEYWORD and self.peek().value == "নইলে":
            self.advance()
            self.expect(DELIM, ":")
            self.expect(NEWLINE)
            self.expect(INDENT)
            while self.peek().type != DEDENT:
                if self.peek().type == NEWLINE:
                    self.advance()
                    continue
                orelse.append(self.parse_statement())
            self.expect(DEDENT)
        return If(test=test, body=body, orelse=orelse, lineno=kw.lineno, col=kw.col)

    def parse_while(self):
        kw = self.expect(KEYWORD)
        test = self.parse_expression()
        self.expect(DELIM, ":")
        self.expect(NEWLINE)
        self.expect(INDENT)
        body = []
        while self.peek().type != DEDENT:
            if self.peek().type == NEWLINE:
                self.advance()
                continue
            body.append(self.parse_statement())
        self.expect(DEDENT)
        return While(test=test, body=body, lineno=kw.lineno, col=kw.col)

    def parse_return(self):
        kw = self.expect(KEYWORD)
        if self.peek().type == NEWLINE:
            self.advance()
            return Return(value=None, lineno=kw.lineno, col=kw.col)
        value = self.parse_expression()
        return Return(value=value, lineno=kw.lineno, col=kw.col)

    # Expressions (precedence climbing)
    def parse_expression(self):
        return self.parse_logic_or()

    def parse_logic_or(self):
        node = self.parse_logic_and()
        while self.peek().type == KEYWORD and self.peek().value == "বা":
            op = self.advance().value
            right = self.parse_logic_and()
            node = BinaryOp(left=node, op=op, right=right)
        return node

    def parse_logic_and(self):
        node = self.parse_equality()
        while self.peek().type == KEYWORD and self.peek().value == "এবং":
            op = self.advance().value
            right = self.parse_equality()
            node = BinaryOp(left=node, op=op, right=right)
        return node

    def parse_equality(self):
        node = self.parse_comparison()
        while self.peek().type == OP and self.peek().value in ("==", "!="):
            op = self.advance().value
            right = self.parse_comparison()
            node = BinaryOp(left=node, op=op, right=right)
        return node

    def parse_comparison(self):
        node = self.parse_term()
        while self.peek().type == OP and self.peek().value in ("<", ">", "<=", ">="):
            op = self.advance().value
            right = self.parse_term()
            node = BinaryOp(left=node, op=op, right=right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.peek().type == OP and self.peek().value in ("+", "-"):
            op = self.advance().value
            right = self.parse_factor()
            node = BinaryOp(left=node, op=op, right=right)
        return node

    def parse_factor(self):
        node = self.parse_unary()
        while self.peek().type == OP and self.peek().value in ("*", "/", "%"):
            op = self.advance().value
            right = self.parse_unary()
            node = BinaryOp(left=node, op=op, right=right)
        return node

    def parse_unary(self):
        if self.peek().type == KEYWORD and self.peek().value == "না":
            op = self.advance().value
            operand = self.parse_unary()
            return UnaryOp(op=op, operand=operand)
        return self.parse_primary()

    def parse_primary(self):
        tok = self.peek()
        if tok.type == NUMBER:
            self.advance()
            return Literal(value=tok.value, typ="number", lineno=tok.lineno, col=tok.col)
        if tok.type == STRING:
            self.advance()
            return Literal(value=tok.value, typ="string", lineno=tok.lineno, col=tok.col)
        if tok.type == BOOL:
            self.advance()
            return Literal(value=tok.value, typ="bool", lineno=tok.lineno, col=tok.col)
        if tok.type == NIL:
            self.advance()
            return Literal(value=None, typ="nil", lineno=tok.lineno, col=tok.col)
        if tok.type == IDENT or (tok.type == KEYWORD and tok.value == "দেখাও"):
            # function name can be IDENT or builtin keyword 'দেখাও'
            self.advance()
            name = tok.value
            # function call
            if self.peek().type == DELIM and self.peek().value == "(":
                self.advance()
                args = []
                if not (self.peek().type == DELIM and self.peek().value == ")"):
                    while True:
                        args.append(self.parse_expression())
                        if self.peek().type == DELIM and self.peek().value == ",":
                            self.advance()
                            continue
                        break
                self.expect(DELIM, ")")
                return Call(func=Identifier(name=name, lineno=tok.lineno, col=tok.col), args=args, lineno=tok.lineno, col=tok.col)
            return Identifier(name=name, lineno=tok.lineno, col=tok.col)
        if tok.type == DELIM and tok.value == "(":
            self.advance()
            node = self.parse_expression()
            self.expect(DELIM, ")")
            return node
        raise ParseError(f"সিনট্যাক্স ত্রুটি: অপ্রত্যাশিত token '{tok.type}' লাইন {tok.lineno}")


def parse_tokens(tokens: List[Token]) -> Program:
    p = Parser(tokens)
    try:
        return p.parse()
    except IndexError:
        raise ParseError("সিনট্যাক্স ত্রুটি: অপ্রত্যাশিত EOF")
