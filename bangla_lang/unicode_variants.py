"""Bangla keyboard and Unicode variant support for BPL.

This module provides mappings for Bangla keywords and characters that may vary
across different keyboard layouts (Probhat, Avro, NumPad, etc.) and Unicode
normalization forms. The lexer uses these to normalize input and accept all
common variants.

Example: ফাংশন and ফংশন both map to the FUNCTION keyword.
"""
import unicodedata
from typing import Dict, Set


def normalize_bangla_keyword(word: str) -> str:
    """Normalize a Bangla word by decomposing, normalizing, and removing combining marks.
    
    This ensures keywords work across different Bangla keyboard layouts and
    Unicode normalization forms.
    """
    # First normalize to NFD (decomposed) form
    nfd = unicodedata.normalize('NFD', word)
    # Remove combining marks (category Mn, Mc, Me)
    cleaned = ''.join(
        ch for ch in nfd 
        if unicodedata.category(ch) not in ('Mn', 'Mc', 'Me')
    )
    # Normalize back to NFC (composed) form
    return unicodedata.normalize('NFC', cleaned)


# Mapping of Bangla keyword variants to canonical form.
# Each key is a variant (from different keyboard layouts or spellings),
# each value is the canonical keyword.
KEYWORD_VARIANTS: Dict[str, str] = {
    # if keyword
    'যদি': 'যদি',
    
    # else keyword
    'নইলে': 'নইলে',
    'অন্যথায়': 'নইলে',  # alternative Bangla word for else
    'নইতো': 'নইলে',  # colloquial variant
    
    # while keyword
    'যখন': 'যখন',
    'যতক্ষণ': 'যখন',  # alternative: "as long as"
    
    # function keyword
    'ফাংশন': 'ফাংশন',
    'ফংশন': 'ফাংশন',  # variant without nukta
    'ফাংশণ': 'ফাংশন',  # variant with different ending
    
    # return keyword
    'ফলাফল': 'ফলাফল',
    'ফেরত': 'ফলাফল',  # alternative: "give back"
    'রিটার্ন': 'ফলাফল',  # transliterated variant
    
    # true keyword
    'সত্য': 'সত্য',
    'সঁচা': 'সত্য',  # colloquial variant
    'ঠিক': 'সত্য',  # alternative: "correct"
    
    # false keyword
    'মিথ্যা': 'মিথ্যা',
    'মিথা': 'মিথ্যা',  # variant without nukta
    'ভুল': 'মিথ্যা',  # alternative: "wrong"
    
    # null/nil keyword
    'নিল': 'নিল',
    'শূন্য': 'নিল',  # alternative: "empty/zero"
    'কোনো': 'নিল',  # alternative: "nothing"
    
    # print keyword
    'দেখাও': 'দেখাও',
    'মুদ্রণ': 'দেখাও',  # legacy keyword
    'প্রিন্ট': 'দেখাও',  # transliterated variant
    'ছাপো': 'দেখাও',  # alternative: "print/write"
}

# Logical operators (Bangla)
LOGICAL_OPERATORS: Dict[str, str] = {
    'এবং': 'এবং',  # and
    'এবাং': 'এবং',  # variant
    'ও': 'এবং',  # alternative: "and"
    
    'বা': 'বা',  # or
    'অথবা': 'বা',  # alternative: "or"
    'অথবো': 'বা',  # variant
    
    'না': 'না',  # not
    'নয়': 'না',  # alternative: "not"
}

# All keywords (canonical forms)
CANONICAL_KEYWORDS: Set[str] = {
    'যদি', 'নইলে', 'যখন', 'ফাংশন', 'ফলাফল',
    'সত্য', 'মিথ্যা', 'নিল', 'দেখাও'
}

# All logical operators (canonical forms)
CANONICAL_LOGICAL_OPS: Set[str] = {
    'এবং', 'বা', 'না'
}

# Normalize mapping keys so lookups are consistent across Unicode forms
_NORM_KEYWORD_VARIANTS: Dict[str, str] = {}
for k, v in KEYWORD_VARIANTS.items():
    _NORM_KEYWORD_VARIANTS[normalize_bangla_keyword(k)] = v

_NORM_LOGICAL_OPERATORS: Dict[str, str] = {}
for k, v in LOGICAL_OPERATORS.items():
    _NORM_LOGICAL_OPERATORS[normalize_bangla_keyword(k)] = v


def get_canonical_keyword(word: str) -> str:
    """Given a Bangla word, return the canonical keyword form if it's a variant.
    
    Returns the canonical form if the word is a known keyword variant,
    otherwise returns the word unchanged.
    """
    normalized = normalize_bangla_keyword(word)
    return _NORM_KEYWORD_VARIANTS.get(normalized, word)


def get_canonical_logical_op(word: str) -> str:
    """Given a Bangla word, return the canonical logical operator form if it's a variant."""
    normalized = normalize_bangla_keyword(word)
    return _NORM_LOGICAL_OPERATORS.get(normalized, word)


def is_keyword_variant(word: str) -> bool:
    """Check if a word is any variant of a keyword."""
    normalized = normalize_bangla_keyword(word)
    return normalized in _NORM_KEYWORD_VARIANTS


def is_logical_op_variant(word: str) -> bool:
    """Check if a word is any variant of a logical operator."""
    normalized = normalize_bangla_keyword(word)
    return normalized in _NORM_LOGICAL_OPERATORS
