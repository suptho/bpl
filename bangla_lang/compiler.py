"""Simple AST -> bytecode compiler for BPL (initial subset).

Supports: Program, ExprStmt, Literal, Identifier, Assign, BinaryOp,
Call, FunctionDef. Produces a `CodeObject` consumed by `bytecode.VM`.
"""
from __future__ import annotations

from typing import Any, List, Dict
from .ast import *
from .bytecode import (
    Instruction,
    CodeObject,
    LOAD_CONST,
    LOAD_NAME,
    STORE_NAME,
    POP_TOP,
    BINARY_ADD,
    BINARY_SUB,
    BINARY_MUL,
    BINARY_DIV,
    RETURN_VALUE,
    CALL_FUNCTION,
)


class CompileError(Exception):
    pass


class Compiler:
    def __init__(self):
        self.instructions: List[Instruction] = []
        self.consts: List[Any] = []
        self.names: List[str] = []
        self.argcount = 0

    def add_const(self, value: Any) -> int:
        try:
            idx = self.consts.index(value)
        except ValueError:
            idx = len(self.consts)
            self.consts.append(value)
        return idx

    def add_name(self, name: str) -> int:
        try:
            idx = self.names.index(name)
        except ValueError:
            idx = len(self.names)
            self.names.append(name)
        return idx

    def emit(self, op: str, arg: Any = None) -> None:
        self.instructions.append(Instruction(op, arg))

    def compile(self, node):
        method = f"compile_{type(node).__name__}"
        f = getattr(self, method, None)
        if not f:
            raise CompileError(f"No compiler for node type {type(node).__name__}")
        return f(node)

    def compile_Program(self, node: Program):
        for stmt in node.body or []:
            self.compile(stmt)
        # Ensure a final RETURN_VALUE
        self.emit(RETURN_VALUE)
        return CodeObject(self.instructions, self.consts, self.names, argcount=0)

    def compile_ExprStmt(self, node: ExprStmt):
        self.compile(node.value)
        self.emit(POP_TOP)

    def compile_Literal(self, node: Literal):
        idx = self.add_const(node.value)
        self.emit(LOAD_CONST, idx)

    def compile_Identifier(self, node: Identifier):
        idx = self.add_name(node.name)
        self.emit(LOAD_NAME, idx)

    def compile_Assign(self, node: Assign):
        # Only simple name assignment supported: target is Identifier
        if not isinstance(node.target, Identifier):
            raise CompileError("Only simple identifier assignments supported")
        self.compile(node.value)
        idx = self.add_name(node.target.name)
        self.emit(STORE_NAME, idx)

    def compile_BinaryOp(self, node: BinaryOp):
        self.compile(node.left)
        self.compile(node.right)
        op = node.op
        if op == "+":
            self.emit(BINARY_ADD)
        elif op == "-":
            self.emit(BINARY_SUB)
        elif op == "*":
            self.emit(BINARY_MUL)
        elif op == "/":
            self.emit(BINARY_DIV)
        else:
            raise CompileError(f"Unsupported binary op: {op}")

    def compile_Call(self, node: Call):
        # Compile function expression then args
        self.compile(node.func)
        for arg in node.args or []:
            self.compile(arg)
        self.emit(CALL_FUNCTION, len(node.args or []))

    def compile_Return(self, node: Return):
        # Compile the return value if present, else load None
        if node.value is not None:
            self.compile(node.value)
        else:
            idx = self.add_const(None)
            self.emit(LOAD_CONST, idx)
        self.emit(RETURN_VALUE)

    def compile_FunctionDef(self, node: FunctionDef):
        # Compile function body into a nested CodeObject
        comp = Compiler()
        # record argument names in names list positionally
        for p in node.params or []:
            comp.add_name(p)
        for stmt in node.body or []:
            comp.compile(stmt)
        comp.emit(RETURN_VALUE)
        func_code = CodeObject(comp.instructions, comp.consts, comp.names, argcount=len(node.params or []))
        const_idx = self.add_const(func_code)
        self.emit(LOAD_CONST, const_idx)
        name_idx = self.add_name(node.name)
        self.emit(STORE_NAME, name_idx)
