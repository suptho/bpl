import sys
import io

from bangla_lang.lexer import Lexer
from bangla_lang.parser import Parser
from bangla_lang.compiler import Compiler
from bangla_lang.bytecode import VM
from bangla_lang import runtime


def run_source_and_capture(source: str):
    lex = Lexer(source)
    tokens = lex.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    comp = Compiler()
    codeobj = comp.compile(ast)
    # Bind builtins into VM
    builtins = {"দেখাও": runtime.bpl_print, "প্রকার": runtime.bpl_type}
    vm = VM(builtins=builtins)
    # Capture stdout
    old = sys.stdout
    sys.stdout = io.StringIO()
    try:
        vm.run_code(codeobj, globals_={})
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old


def test_print_and_add():
    src = 'ফাংশন add(a, b):\n  ফলাফল a + b\n\nদেখাও(add(2, 3))\n'
    out = run_source_and_capture(src)
    assert "5" in out
