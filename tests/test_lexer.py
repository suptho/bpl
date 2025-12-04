import pytest

from bangla_lang.lexer import lex
from bangla_lang.tokens import IDENT, KEYWORD


def test_bangla_identifier():
    src = "পরীক্ষা = ১"
    toks = lex(src)
    # Find first IDENT token
    assert any(t.type == IDENT and t.value == "পরীক্ষা" for t in toks)


def test_keyword_jodi():
    src = "যদি সত্য:\n    মুদ্রণ(\"ok\")"
    toks = lex(src)
    assert any(t.type == KEYWORD and t.value == "যদি" for t in toks)
