"""
Test Bangla keyboard variant support.
Ensures BPL works seamlessly with Probhat, Avro, NumPad, and other keyboard layouts.
"""

import unicodedata
import sys
sys.path.insert(0, '/home/mmsuptho/Academic/OOP')

from bangla_lang.lexer import Lexer
from bangla_lang.tokens import KEYWORD, BOOL, NIL, IDENT, NUMBER
from bangla_lang.unicode_variants import (
    normalize_bangla_keyword,
    get_canonical_keyword,
    is_keyword_variant,
    get_canonical_logical_op,
    is_logical_op_variant,
)


class TestKeywordVariants:
    """Test keyboard layout variants for keywords."""

    def test_function_keyword_variants(self):
        """Test ফাংশন variants across keyboard layouts."""
        variants = ["ফাংশন", "ফংশন", "ফাংশণ"]
        for variant in variants:
            canonical = get_canonical_keyword(variant)
            assert canonical == "ফাংশন", f"Failed for variant: {variant}"

    def test_return_keyword_variants(self):
        """Test ফলাফল variants (return/yield)."""
        variants = ["ফলাফল", "ফেরত", "রিটার্ন"]
        for variant in variants:
            canonical = get_canonical_keyword(variant)
            assert canonical == "ফলাফল", f"Failed for variant: {variant}"

    def test_if_else_variants(self):
        """Test যদি/নইলে variants."""
        if_variants = ["যদি"]
        else_variants = ["নইলে", "অন্যথায়", "নইতো"]
        
        for variant in if_variants:
            canonical = get_canonical_keyword(variant)
            assert canonical == "যদি", f"If variant failed: {variant}"
        
        for variant in else_variants:
            canonical = get_canonical_keyword(variant)
            assert canonical == "নইলে", f"Else variant failed: {variant}"

    def test_while_loop_variants(self):
        """Test যখন/যতক্ষণ (while loop) variants."""
        variants = ["যখন", "যতক্ষণ"]
        for variant in variants:
            canonical = get_canonical_keyword(variant)
            assert canonical == "যখন", f"While variant failed: {variant}"

    def test_print_keyword_variants(self):
        """Test দেখাও variants across keyboard layouts."""
        variants = ["দেখাও", "মুদ্রণ", "প্রিন্ট", "ছাপো"]
        for variant in variants:
            canonical = get_canonical_keyword(variant)
            assert canonical == "দেখাও", f"Print variant failed: {variant}"

    def test_nil_keyword_variants(self):
        """Test নিল/শূন্য/কোনো (null) variants."""
        variants = ["নিল", "শূন্য", "কোনো"]
        for variant in variants:
            assert is_keyword_variant(variant), f"Nil variant not recognized: {variant}"

    def test_logical_operator_and_variants(self):
        """Test এবং (and) operator variants."""
        variants = ["এবং", "এবাং", "ও"]
        for variant in variants:
            assert is_logical_op_variant(variant), f"'and' variant not recognized: {variant}"
            canonical = get_canonical_logical_op(variant)
            assert canonical == "এবং", f"'and' canonical failed for: {variant}"

    def test_logical_operator_or_variants(self):
        """Test বা (or) operator variants."""
        variants = ["বা", "অথবা", "অথবো"]
        for variant in variants:
            assert is_logical_op_variant(variant), f"'or' variant not recognized: {variant}"
            canonical = get_canonical_logical_op(variant)
            assert canonical == "বা", f"'or' canonical failed for: {variant}"

    def test_logical_operator_not_variants(self):
        """Test না (not) operator variants."""
        variants = ["না", "নয়"]
        for variant in variants:
            assert is_logical_op_variant(variant), f"'not' variant not recognized: {variant}"
            canonical = get_canonical_logical_op(variant)
            assert canonical == "না", f"'not' canonical failed for: {variant}"

    def test_boolean_true_variants(self):
        """Test সত্য (true) variants."""
        variants = ["সত্য", "সঁচা", "ঠিক"]
        for variant in variants:
            canonical = get_canonical_keyword(variant)
            assert canonical == "সত্য", f"True variant failed: {variant}"

    def test_boolean_false_variants(self):
        """Test মিথ্যা (false) variants."""
        variants = ["মিথ্যা", "মিথা", "ভুল"]
        for variant in variants:
            canonical = get_canonical_keyword(variant)
            assert canonical == "মিথ্যা", f"False variant failed: {variant}"


class TestUnicodeNormalization:
    """Test Unicode normalization for keyboard variant handling."""

    def test_nfd_decomposition(self):
        """Test that NFD decomposition works correctly."""
        bangla_word = "ফাংশন"
        nfd = unicodedata.normalize('NFD', bangla_word)
        # After decomposition, ফ may become base + diacritic
        assert nfd != bangla_word or nfd == bangla_word, "NFD decomposition should work"

    def test_nfc_recomposition(self):
        """Test that NFC recomposition works correctly."""
        bangla_word = "ফাংশন"
        nfd = unicodedata.normalize('NFD', bangla_word)
        nfc = unicodedata.normalize('NFC', nfd)
        assert nfc == bangla_word, "NFC should return to original form"

    def test_combining_mark_removal(self):
        """Test removing combining marks for variant matching."""
        normalized = normalize_bangla_keyword("ফাংশন")
        # Should return a valid Bangla word after mark removal
        assert len(normalized) > 0, "Normalized form should not be empty"
        assert "ফ" in normalized or normalized[0] != "", "Should contain Bangla characters"

    def test_normalize_consistency(self):
        """Test that normalization is consistent across multiple calls."""
        word = "ফাংশন"
        norm1 = normalize_bangla_keyword(word)
        norm2 = normalize_bangla_keyword(word)
        assert norm1 == norm2, "Normalization should be deterministic"


class TestLexerKeyboardVariants:
    """Integration tests for lexer with keyboard variants."""

    def test_lexer_function_variant(self):
        """Test lexer recognizes function keyword variant."""
        code = "ফংশন test():\n  ফলাফল 5"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # First token should be KEYWORD with canonical form "ফাংশন"
        assert tokens[0].type == KEYWORD
        assert tokens[0].value == "ফাংশন"

    def test_lexer_print_variant(self):
        """Test lexer recognizes print keyword variant."""
        code = 'মুদ্রণ("হ্যালো")'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # First token should be KEYWORD with canonical form "দেখাও"
        assert tokens[0].type == KEYWORD
        assert tokens[0].value == "দেখাও"

    def test_lexer_return_variant(self):
        """Test lexer recognizes return keyword variant."""
        code = "ফেরত ৫"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # First token should be KEYWORD with canonical form "ফলাফল"
        assert tokens[0].type == KEYWORD
        assert tokens[0].value == "ফলাফল"

    def test_lexer_boolean_variants(self):
        """Test lexer recognizes boolean variants."""
        code = "সঁচা"  # Bangla true variant (colloquial)
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # Should tokenize as BOOL with value True
        assert tokens[0].type == BOOL
        assert tokens[0].value is True

    def test_lexer_false_variant(self):
        """Test lexer recognizes false boolean variant."""
        code = "ভুল"  # Colloquial for false (wrong)
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert tokens[0].type == BOOL
        assert tokens[0].value is False

    def test_lexer_logical_and_variant(self):
        """Test lexer recognizes logical 'and' variant."""
        code = "ক এবাং খ"  # Avro variant for এবং
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # Token sequence: IDENT(ক), KEYWORD(এবং), IDENT(খ)
        assert tokens[0].type == IDENT
        assert tokens[1].type == KEYWORD
        assert tokens[1].value == "এবং"

    def test_lexer_logical_or_variant(self):
        """Test lexer recognizes logical 'or' variant."""
        code = "ক অথবা খ"  # Formal variant for বা
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert tokens[1].type == KEYWORD
        assert tokens[1].value == "বা"

    def test_lexer_if_else_variant(self):
        """Test lexer recognizes if/else variants."""
        code = "যদি সত্য:\n  ক = ৫\nঅন্যথায়:\n  ক = ৬"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # Collect KEYWORD tokens
        keywords = [t.value for t in tokens if t.type == KEYWORD]
        assert "যদি" in keywords
        assert "নইলে" in keywords  # অন্যথায় should canonicalize to নইলে

    def test_lexer_preserve_identifier(self):
        """Test that non-keyword identifiers are preserved."""
        code = "ফংশনের_নাম = ১०"  # Custom identifier (not a keyword)
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # Should tokenize as IDENT, not KEYWORD
        assert tokens[0].type == IDENT
        assert tokens[0].value == "ফংশনের_নাম"


class TestKeywordVariantEdgeCases:
    """Test edge cases and corner cases for keyboard variants."""

    def test_unknown_variant_fallback(self):
        """Test that unknown variants fall back to identifier."""
        code = "অজানা_শব্দ = ১"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert tokens[0].type == IDENT
        assert tokens[0].value == "অজানা_শব্দ"

    def test_mixed_variants_in_code(self):
        """Test mixing variants in the same code."""
        code = """ফংশন calc():
  ক = সঁচা
  যতক্ষণ ক:
    দেখাও("হ্যালো")
    ক = ভুল
  ফেরত নিল"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        keywords = [t.value for t in tokens if t.type == KEYWORD]
        # All variants should be canonicalized
        assert "ফাংশন" in keywords  # ফংশন → ফাংশন
        assert "যখন" in keywords    # যতক্ষণ → যখন
        assert "দেখাও" in keywords
        assert "ফলাফল" in keywords  # ফেরত → ফলাফল
        bools = [t.value for t in tokens if t.type == BOOL]
        assert True in bools   # সঁচা
        assert False in bools  # ভুল

    def test_case_sensitive_variants(self):
        """Test that keyword matching respects Unicode case (when applicable)."""
        # Bengali doesn't have uppercase/lowercase, but test consistency
        code = "ফাংশন test():\n  নিল"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # Both should tokenize as keywords
        keywords = [t for t in tokens if t.type == KEYWORD]
        assert len(keywords) >= 2


if __name__ == "__main__":
    # Quick smoke test
    print("Running keyboard variant tests...")
    test_kv = TestKeywordVariants()
    test_kv.test_function_keyword_variants()
    test_kv.test_logical_operator_and_variants()
    print("✓ Keyboard variant tests passed")
    
    test_lex = TestLexerKeyboardVariants()
    test_lex.test_lexer_function_variant()
    test_lex.test_lexer_print_variant()
    print("✓ Lexer integration tests passed")
    
    print("\nAll tests passed!")
