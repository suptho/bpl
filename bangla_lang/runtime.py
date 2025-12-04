"""Built-in runtime helpers for BPL."""
from typing import Any


def bpl_print(*args: Any) -> None:
    # Print arguments separated by space, support unicode strings
    out = " ".join(str(a) for a in args)
    print(out, flush=True)


def bpl_type(x: Any) -> str:
    if x is None:
        return "নিল"
    if isinstance(x, bool):
        return "বুলীয়ান"
    if isinstance(x, int):
        return "ইন্ট"
    if isinstance(x, float):
        return "ফ্লোট"
    if isinstance(x, str):
        return "স্ট্রিং"
    return "অজানা"  # for functions/objects
