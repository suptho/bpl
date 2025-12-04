import pytest

from bangla_lang.lexer import lex
from bangla_lang.parser import parse_tokens


def test_parse_simple_assign():
    src = "x = 1\n"
    toks = lex(src)
    ast = parse_tokens(toks)
    assert ast is not None


def test_parse_function_def():
    src = "ఫাংশন add(a, b):\n    ফলাফল a + b\n"
    toks = lex(src)
    ast = parse_tokens(toks)
    assert ast is not None
