from __future__ import annotations

import re


TOKEN_PATTERN = re.compile(r"[a-z]+(?:'[a-z]+)?|\d+")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())
