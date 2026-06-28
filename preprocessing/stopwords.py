from __future__ import annotations

from config import DATASET, NEGATIONS, QUESTION_WORDS, TIME_WORDS
from preprocessing.pos_tagger import TaggedToken
from utils.helpers import safe_load_json


PRESERVE_POS = {"NOUN", "PROPN", "VERB", "ADJ", "ADV", "NUM", "WH", "NEG", "TIME"}
PRESERVE_WORDS = QUESTION_WORDS | NEGATIONS | TIME_WORDS | {"i", "you", "me", "my", "your"}


def load_stopwords() -> set[str]:
    words = safe_load_json(DATASET.stopwords, [])
    return {str(word).lower() for word in words}


def remove_stopwords(tagged_tokens: list[TaggedToken], stopwords: set[str] | None = None) -> list[TaggedToken]:
    stopwords = stopwords if stopwords is not None else load_stopwords()
    filtered: list[TaggedToken] = []
    for token in tagged_tokens:
        if token.text in stopwords and token.text not in PRESERVE_WORDS:
            continue
        if token.text in PRESERVE_WORDS or token.pos in PRESERVE_POS:
            filtered.append(token)
            continue
        filtered.append(token)
    return filtered
