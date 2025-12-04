"""Simple REPL for Bangla Programming Language (BPL).

For now the REPL tokenizes input and prints tokens; later it will parse and
evaluate code.
"""
import readline
import os
from typing import List

from .lexer import lex
from .runtime import bpl_print
from .cli import run_source, run_file

HISTORY = os.path.expanduser("~/.bpl_history")
PROMPT = "বিপিএল> "
CONT_PROMPT = "...> "


def load_history():
    try:
        readline.read_history_file(HISTORY)
    except FileNotFoundError:
        pass


def save_history():
    try:
        readline.write_history_file(HISTORY)
    except Exception:
        pass


def repl():
    load_history()
    try:
        while True:
            try:
                src = input(PROMPT)
            except EOFError:
                print()
                break
            if not src.strip():
                continue
            if src.strip() in ("exit", "প্রস্থান"):
                break
            # Try to run the source line (simple) using runner
            try:
                # run_source expects full source; for REPL we'll try to run a single line
                run_source(src)
            except Exception as e:
                print(str(e))
    finally:
        save_history()


if __name__ == "__main__":
    repl()


def run_file_entry(path: str):
    return run_file(path)


def run_source_entry(source: str):
    return run_source(source)
