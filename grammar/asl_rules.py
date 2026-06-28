from __future__ import annotations

from config import QUESTION_WORDS
from utils.helpers import unique_preserve_order


def apply_asl_order(tokens: list[str]) -> list[str]:
    if not tokens:
        return []

    question_tokens = [token for token in tokens if token in QUESTION_WORDS]
    body = [token for token in tokens if token not in QUESTION_WORDS]
    ordered = body + question_tokens
    return unique_preserve_order(ordered)


def tokens_to_gloss(tokens: list[str]) -> str:
    return " ".join(token.upper() for token in tokens)
