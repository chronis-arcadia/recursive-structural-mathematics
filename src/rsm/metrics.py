"""Small dependency-free drift metrics used by the RSM reference implementation."""

from __future__ import annotations

from difflib import SequenceMatcher
import re
import zlib


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def sequence_distance(a: str, b: str) -> float:
    """Return 1 - SequenceMatcher ratio, normalized to [0, 1]."""
    return _clip01(1.0 - SequenceMatcher(None, a, b).ratio())


def token_jaccard_distance(a: str, b: str) -> float:
    """Set-based token Jaccard distance.

    This deliberately ignores token order. It is useful as one component,
    not as a general semantic metric.
    """
    tokenize = lambda text: set(re.findall(r"\w+", text.casefold()))
    left, right = tokenize(a), tokenize(b)
    if not left and not right:
        return 0.0
    union = left | right
    return _clip01(1.0 - (len(left & right) / len(union)))


def compression_length_delta(a: str, b: str) -> float:
    """Normalized delta between zlib-compressed byte lengths.

    This is a description-length proxy. It is not Kolmogorov complexity
    and is not an information-theoretic entropy estimate.
    """
    la = len(zlib.compress(a.encode("utf-8")))
    lb = len(zlib.compress(b.encode("utf-8")))
    return _clip01(abs(la - lb) / max(la, lb, 1))
