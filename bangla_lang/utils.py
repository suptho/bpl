import unicodedata


def normalize_unicode(s: str) -> str:
    """Normalize source text to NFC for consistent tokenization."""
    return unicodedata.normalize("NFC", s)


def is_identifier_start(ch: str) -> bool:
    """Return True if character can start an identifier (letter or underscore).
    Accepts Bangla letters because they are category 'L'."""
    if not ch:
        return False
    if ch == "_":
        return True
    return ch.isalpha()


def is_identifier_part(ch: str) -> bool:
    """Return True if character can be part of identifier (letter, digit, underscore, combining marks)."""
    if not ch:
        return False
    if ch == "_":
        return True
    if ch.isalpha() or ch.isdigit():
        return True
    cat = unicodedata.category(ch)
    # Combining mark categories: Mc, Mn
    if cat in ("Mc", "Mn"):
        return True
    return False
