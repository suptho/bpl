"""Simple bytecode VM for BPL (initial implementation).

This is an initial stack-based bytecode VM and CodeObject representation.
It is intentionally small so we can iterate: supports constants, names,
basic binary ops, function definitions (as nested CodeObject), and CALL/RETURN.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import types


# Opcode names
LOAD_CONST = "LOAD_CONST"
LOAD_NAME = "LOAD_NAME"
STORE_NAME = "STORE_NAME"
POP_TOP = "POP_TOP"
BINARY_ADD = "BINARY_ADD"
BINARY_SUB = "BINARY_SUB"
BINARY_MUL = "BINARY_MUL"
BINARY_DIV = "BINARY_DIV"
RETURN_VALUE = "RETURN_VALUE"
CALL_FUNCTION = "CALL_FUNCTION"


@dataclass
class Instruction:
    op: str
    arg: Any = None


@dataclass
class CodeObject:
    instructions: List[Instruction]
    consts: List[Any]
    names: List[str]
    argcount: int = 0


class Frame:
    def __init__(self, code: CodeObject, globals_: Dict[str, Any], locals_: Dict[str, Any]):
        self.code = code
        self.globals = globals_
        self.locals = locals_
        self.stack: List[Any] = []
        self.pc = 0


class VMError(Exception):
    pass


class VM:
    def __init__(self, builtins: Dict[str, Any] | None = None):
        # Lazy import runtime to avoid circular imports at module load time
        try:
            from . import runtime as _runtime
        except Exception:
            _runtime = None

        self.frames: List[Frame] = []
        # Default builtins from runtime if available
        default_builtins: Dict[str, Any] = {}
        if _runtime is not None:
            default_builtins = {"দেখাও": _runtime.bpl_print, "প্রকার": _runtime.bpl_type}

        # Merge provided builtins over defaults
        self.builtins = {**default_builtins, **(builtins or {})}

    def run_code(self, code: CodeObject, globals_: Dict[str, Any] | None = None, locals_: Dict[str, Any] | None = None):
        globals_ = globals_ or {}
        locals_ = locals_ or {}
        frame = Frame(code, globals_, locals_)
        self.frames.append(frame)
        try:
            return self.run_frame(frame)
        finally:
            self.frames.pop()

    def run_frame(self, frame: Frame):
        stack = frame.stack
        instrs = frame.code.instructions
        consts = frame.code.consts
        names = frame.code.names

        while frame.pc < len(instrs):
            ins = instrs[frame.pc]
            frame.pc += 1
            op = ins.op
            arg = ins.arg

            if op == LOAD_CONST:
                stack.append(consts[arg])
                continue

            if op == LOAD_NAME:
                name = names[arg]
                if name in frame.locals:
                    stack.append(frame.locals[name])
                elif name in frame.globals:
                    stack.append(frame.globals[name])
                elif name in self.builtins:
                    stack.append(self.builtins[name])
                else:
                    raise VMError(f"NameError: {name}")
                continue

            if op == STORE_NAME:
                name = names[arg]
                val = stack.pop()
                frame.locals[name] = val
                continue

            if op == POP_TOP:
                stack.pop()
                continue

            if op in (BINARY_ADD, BINARY_SUB, BINARY_MUL, BINARY_DIV):
                b = stack.pop()
                a = stack.pop()
                if op == BINARY_ADD:
                    stack.append(a + b)
                elif op == BINARY_SUB:
                    stack.append(a - b)
                elif op == BINARY_MUL:
                    stack.append(a * b)
                elif op == BINARY_DIV:
                    stack.append(a / b)
                continue

            if op == CALL_FUNCTION:
                argcount = arg
                args = [stack.pop() for _ in range(argcount)][::-1]
                func = stack.pop()
                # If func is a CodeObject (user-defined), create a new frame
                if isinstance(func, CodeObject):
                    # Prepare globals for function as a shallow copy of caller globals
                    new_globals = dict(frame.globals)
                    # Prepare locals with parameters already bound by compiler
                    fn_locals: Dict[str, Any] = {}
                    # The compiler stores parameter names in func.names (positional at start)
                    for i, v in enumerate(args[: func.argcount]):
                        if i < len(func.names):
                            param = func.names[i]
                            fn_locals[param] = v

                    res = self.run_code(func, new_globals, fn_locals)
                    stack.append(res)
                elif callable(func):
                    # Builtin Python callable
                    res = func(*args)
                    stack.append(res)
                else:
                    raise VMError("Attempt to call non-callable")
                continue

            if op == RETURN_VALUE:
                val = stack.pop() if stack else None
                return val

            raise VMError(f"Unknown opcode: {op}")

        return None
