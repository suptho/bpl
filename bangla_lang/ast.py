from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class Node:
    lineno: int = 0
    col: int = 0


@dataclass
class Program(Node):
    body: List[Any] = None


@dataclass
class FunctionDef(Node):
    name: str = ""
    params: List[str] = None
    body: List[Any] = None


@dataclass
class If(Node):
    test: Any = None
    body: List[Any] = None
    orelse: List[Any] = None


@dataclass
class While(Node):
    test: Any = None
    body: List[Any] = None


@dataclass
class Return(Node):
    value: Any = None


@dataclass
class Assign(Node):
    target: Any = None
    value: Any = None


@dataclass
class ExprStmt(Node):
    value: Any = None


@dataclass
class BinaryOp(Node):
    left: Any = None
    op: str = ""
    right: Any = None


@dataclass
class UnaryOp(Node):
    op: str = ""
    operand: Any = None


@dataclass
class Call(Node):
    func: Any = None
    args: List[Any] = None


@dataclass
class Identifier(Node):
    name: str = ""


@dataclass
class Literal(Node):
    value: Any = None
    typ: str = ""
