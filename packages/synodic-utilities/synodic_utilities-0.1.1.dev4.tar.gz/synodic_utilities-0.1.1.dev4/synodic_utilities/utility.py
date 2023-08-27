"""Utility definitions"""

import re
from typing import NamedTuple

_canonicalize_regex = re.compile(r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))")


class NormalizedName(NamedTuple):
    """Normalized name"""

    name: str
    group: str


def canonicalize_name(name: str) -> NormalizedName:
    """Performs normalization on an input string

    Args:
        name: The string to parse

    Returns:
        The normalized name
    """

    sub = re.sub(_canonicalize_regex, r" \1", name)
    values = sub.split(" ")
    result = "".join(values[:-1])
    return NormalizedName(result.lower(), values[-1].lower())
