"""Evaluator skeleton for BPL.

Contains an `Environment` class and minimal evaluator functions to be extended.
"""
from typing import Any, Dict, Optional

from .errors import RuntimeErrorBPL
from .ast import Program, ExprStmt, Assign, Identifier, Literal, BinaryOp, UnaryOp, Call, FunctionDef, If, While, Return
from .runtime import bpl_print, bpl_type


class ReturnException(Exception):
    def __init__(self, value: Any):
        self.value = value


class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.vars: Dict[str, Any] = {}
        self.parent = parent

    def define(self, name: str, value: Any):
        self.vars[name] = value

    def set(self, name: str, value: Any):
        env = self.find(name)
        if env is None:
            raise RuntimeErrorBPL(f"নাম ত্রুটি: অপরিচিত নাম '{name}'")
        env.vars[name] = value

    def get(self, name: str) -> Any:
        env = self.find(name)
        if env is None:
            raise RuntimeErrorBPL(f"নাম ত্রুটি: অপরিচিত নাম '{name}'")
        return env.vars[name]

    def find(self, name: str) -> Optional['Environment']:
        if name in self.vars:
            return self
        if self.parent:
            return self.parent.find(name)
        return None


class Function:
    def __init__(self, name: str, params, body, env: Environment):
        self.name = name
        self.params = params
        self.body = body
        self.env = env

    def call(self, args, evaluator):
        if len(args) != len(self.params):
            raise RuntimeErrorBPL(f"রানটাইম ত্রুটি: {self.name} প্রত্যাশা {len(self.params)} আর্গুমেন্ট কিন্তু পেয়েছে {len(args)}")
        local = Environment(parent=self.env)
        for n, v in zip(self.params, args):
            local.define(n, v)
        try:
            for stmt in self.body:
                evaluator.eval_statement(stmt, local)
        except ReturnException as r:
            return r.value
        return None


class Evaluator:
    def __init__(self):
        self.global_env = Environment()
        # register builtins
        self.global_env.define("দেখাও", bpl_print)
        self.global_env.define("প্রকার", bpl_type)

    def eval(self, node, env: Optional[Environment] = None):
        if env is None:
            env = self.global_env
        if isinstance(node, Program):
            for stmt in node.body:
                self.eval_statement(stmt, env)
            return None
        raise RuntimeErrorBPL("রানটাইম ত্রুটি: অনির্ণীত নোড")

    def eval_statement(self, stmt, env: Environment):
        if isinstance(stmt, ExprStmt):
            return self.eval_expression(stmt.value, env)
        if isinstance(stmt, Assign):
            val = self.eval_expression(stmt.value, env)
            if isinstance(stmt.target, Identifier):
                env.define(stmt.target.name, val)
                return val
            raise RuntimeErrorBPL("সিনট্যাক্স ত্রুটি: অপর্যাপ্ত অ্যাসাইনউপাদান")
        if isinstance(stmt, FunctionDef):
            fn = Function(stmt.name, stmt.params or [], stmt.body or [], env)
            env.define(stmt.name, fn)
            return None
        if isinstance(stmt, If):
            cond = self.eval_expression(stmt.test, env)
            if self.is_truthy(cond):
                for s in stmt.body:
                    self.eval_statement(s, env)
            else:
                for s in stmt.orelse or []:
                    self.eval_statement(s, env)
            return None
        if isinstance(stmt, While):
            while self.is_truthy(self.eval_expression(stmt.test, env)):
                for s in stmt.body:
                    self.eval_statement(s, env)
            return None
        if isinstance(stmt, Return):
            val = None
            if stmt.value is not None:
                val = self.eval_expression(stmt.value, env)
            raise ReturnException(val)
        raise RuntimeErrorBPL(f"রানটাইম ত্রুটি: অপরিচিত স্টেটমেন্ট {type(stmt)}")

    def eval_expression(self, expr, env: Environment):
        if isinstance(expr, Literal):
            return expr.value
        if isinstance(expr, Identifier):
            # lookup
            return env.get(expr.name)
        if isinstance(expr, BinaryOp):
            left = self.eval_expression(expr.left, env)
            right = self.eval_expression(expr.right, env)
            op = expr.op
            try:
                if op == "+":
                    return left + right
                if op == "-":
                    return left - right
                if op == "*":
                    return left * right
                if op == "/":
                    return left / right
                if op == "%":
                    return left % right
                if op == "==":
                    return left == right
                if op == "!=":
                    return left != right
                if op == "<":
                    return left < right
                if op == ">":
                    return left > right
                if op == "<=":
                    return left <= right
                if op == ">=":
                    return left >= right
                # logical Bangla operators
                if op == "বা":
                    return self.is_truthy(left) or self.is_truthy(right)
                if op == "এবং":
                    return self.is_truthy(left) and self.is_truthy(right)
            except Exception as e:
                raise RuntimeErrorBPL(f"টাইপ ত্রুটি: {e}")
        if isinstance(expr, UnaryOp):
            val = self.eval_expression(expr.operand, env)
            if expr.op == "না":
                return not self.is_truthy(val)
            raise RuntimeErrorBPL(f"অজানা ইউনারি অপারেটর {expr.op}")
        if isinstance(expr, Call):
            # func can be Identifier with name or builtins
            func_obj = None
            if isinstance(expr.func, Identifier):
                try:
                    func_obj = env.get(expr.func.name)
                except RuntimeErrorBPL:
                    func_obj = None
            # if builtin registered in global env
            if func_obj is None and expr.func.name in self.global_env.vars:
                func_obj = self.global_env.get(expr.func.name)

            args = [self.eval_expression(a, env) for a in expr.args or []]
            # if Python callable builtin
            if callable(func_obj):
                return func_obj(*args)
            # if user Function
            if isinstance(func_obj, Function):
                return func_obj.call(args, self)
            raise RuntimeErrorBPL(f"নাম ত্রুটি: অপরিচিত ফাংশন '{expr.func.name}'")
        raise RuntimeErrorBPL("রানটাইম ত্রুটি: অপরিচিত এক্সপ্রেশন")

    def is_truthy(self, v):
        if v is None:
            return False
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return v != 0
        if isinstance(v, str):
            return v != ""
        return True


def run_program(ast: Program):
    ev = Evaluator()
    return ev.eval(ast)
