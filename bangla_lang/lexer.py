"""Simple lexer for Bangla Programming Language (BPL).

This lexer normalizes Unicode input and tokenizes identifiers (Bangla or Latin),
numbers, strings, keywords, operators, and produces INDENT/DEDENT tokens using
a Python-like indentation model.

This is a practical, beginner-friendly implementation and is intentionally
small and easy to read so it can be extended.
"""
from __future__ import annotations

import unicodedata
from typing import List, Iterator, Optional

from .tokens import Token, INDENT, DEDENT, NEWLINE, EOF, IDENT, NUMBER, STRING, KEYWORD, OP, DELIM, BOOL, NIL
from .utils import normalize_unicode, is_identifier_start, is_identifier_part
from .errors import LexError


# Bangla keywords mapping
KEYWORDS = {
    "যদি",
    "নইলে",
    "যখন",
    "ফাংশন",
    "ফলাফল",
    "সত্য",
    "মিথ্যা",
    "নিল",
    "দেখাও",
}

# Operators (longest-first will be matched)
OPERATORS = ["==", "!=", "<=", ">=", "+", "-", "*", "/", "%", "<", ">", "="]
DELIMITERS = {"(", ")", ":", ","}


class Lexer:
    def __init__(self, source: str, filename: str = "<input>"):
        self.source = normalize_unicode(source)
        self.filename = filename
        # We'll operate line-by-line to simplify indentation handling
        self.lines = self.source.splitlines()
        self.lineno = 0
        self.col = 0
        self.indent_stack = [0]
        self.pending_dedents = 0
        self._tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        for i, raw_line in enumerate(self.lines):
            self.lineno = i + 1
            line = raw_line.rstrip("\n\r")
            # Skip empty lines (but emit NEWLINE so parser can handle)
            if not line.strip():
                # Emit NEWLINE (but do not change indent)
                self._tokens.append(Token(NEWLINE, "\n", self.lineno, 0))
                continue

            # Count leading spaces for indentation (tabs expanded to 4 spaces)
            expanded = line.expandtabs(4)
            indent = len(expanded) - len(expanded.lstrip(" "))
            self.col = indent + 1

            if indent > self.indent_stack[-1]:
                self.indent_stack.append(indent)
                self._tokens.append(Token(INDENT, indent, self.lineno, 0))
            while indent < self.indent_stack[-1]:
                self.indent_stack.pop()
                self._tokens.append(Token(DEDENT, indent, self.lineno, 0))

            # tokenize the content of the line
            i = 0
            text = expanded.lstrip(" ")
            col_offset = indent
            while i < len(text):
                ch = text[i]
                col = col_offset + i + 1
                # Skip spaces between tokens
                if ch.isspace():
                    i += 1
                    continue

                # Comments
                if ch == "#":
                    # comment: skip rest of line
                    break

                # String literal
                if ch == '"' or ch == "'":
                    quote = ch
                    i += 1
                    start = i
                    val_chars = []
                    escaped = False
                    while i < len(text):
                        c = text[i]
                        if escaped:
                            if c == "n":
                                val_chars.append("\n")
                            elif c == "t":
                                val_chars.append("\t")
                            elif c == "\\":
                                val_chars.append("\\")
                            elif c == quote:
                                val_chars.append(quote)
                            else:
                                val_chars.append(c)
                            escaped = False
                            i += 1
                            continue
                        if c == "\\":
                            escaped = True
                            i += 1
                            continue
                        if c == quote:
                            i += 1
                            break
                        val_chars.append(c)
                        i += 1
                    else:
                        raise LexError(f"সিনট্যাক্স ত্রুটি: স্ট্রিং সম্পূর্ণ হয়নি লাইন {self.lineno}")
                    val = "".join(val_chars)
                    self._tokens.append(Token(STRING, val, self.lineno, col))
                    continue

                # Number (integer or float)
                if ch.isdigit():
                    start_i = i
                    while i < len(text) and text[i].isdigit():
                        i += 1
                    if i < len(text) and text[i] == ".":
                        i += 1
                        if i >= len(text) or not text[i].isdigit():
                            raise LexError(f"সিনট্যাক্স ত্রুটি: অবৈধ সংখ্যা লাইন {self.lineno}")
                        while i < len(text) and text[i].isdigit():
                            i += 1
                        tok_text = text[start_i:i]
                        val = float(tok_text)
                    else:
                        tok_text = text[start_i:i]
                        val = int(tok_text)
                    self._tokens.append(Token(NUMBER, val, self.lineno, col))
                    continue

                # Identifier or keyword (Bangla or Latin)
                if is_identifier_start(ch):
                    start_i = i
                    while i < len(text) and is_identifier_part(text[i]):
                        i += 1
                    name = text[start_i:i]
                    if name in ("সত্য", "মিথ্যা"):
                        bval = True if name == "সত্য" else False
                        self._tokens.append(Token(BOOL, bval, self.lineno, col))
                    elif name == "নিল":
                        self._tokens.append(Token(NIL, None, self.lineno, col))
                    elif name in KEYWORDS:
                        self._tokens.append(Token(KEYWORD, name, self.lineno, col))
                    else:
                        self._tokens.append(Token(IDENT, name, self.lineno, col))
                    continue

                # Operators (longest-first)
                matched = False
                for op in sorted(OPERATORS, key=lambda x: -len(x)):
                    if text.startswith(op, i):
                        self._tokens.append(Token(OP, op, self.lineno, col))
                        i += len(op)
                        matched = True
                        break
                if matched:
                    continue

                # Delimiters
                if ch in DELIMITERS:
                    self._tokens.append(Token(DELIM, ch, self.lineno, col))
                    i += 1
                    continue

                # Unknown char
                raise LexError(f"অবৈধ চিহ্ন: '{ch}' লাইন {self.lineno}")

            # At end of line emit NEWLINE
            self._tokens.append(Token(NEWLINE, "\n", self.lineno, len(text) + 1))

        # After all lines, unwind remaining indents
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self._tokens.append(Token(DEDENT, 0, self.lineno, 0))

        self._tokens.append(Token(EOF, None, self.lineno + 1, 0))
        return self._tokens


# Small helper to get tokens from source
def lex(source: str) -> List[Token]:
    l = Lexer(source)
    return l.tokenize()
