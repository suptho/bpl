"""Simple CLI runner for BPL files."""
from pathlib import Path
import sys

from .lexer import lex
from .parser import parse_tokens
from .evaluator import run_program


def run_source(source: str, filename: str = "<input>"):
    tokens = lex(source)
    ast = parse_tokens(tokens)
    return run_program(ast)


def run_file(path: str):
    p = Path(path)
    src = p.read_text(encoding="utf-8")
    return run_source(src, str(p))


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("ব্যবহার: python -m bangla_lang.cli <file.bang>")
        sys.exit(1)
    run_file(sys.argv[1])
