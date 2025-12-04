from dataclasses import dataclass
from typing import Any


@dataclass
class Token:
    type: str
    value: Any
    lineno: int
    col: int

    def __repr__(self) -> str:
        return f"Token({self.type!r}, {self.value!r}, line={self.lineno}, col={self.col})"


# Token type constants
INDENT = "INDENT"
DEDENT = "DEDENT"
NEWLINE = "NEWLINE"
EOF = "EOF"
IDENT = "IDENT"
NUMBER = "NUMBER"
STRING = "STRING"
KEYWORD = "KEYWORD"
OP = "OP"
DELIM = "DELIM"
COMMENT = "COMMENT"
BOOL = "BOOL"
NIL = "NIL"
