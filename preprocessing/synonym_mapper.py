from __future__ import annotations

from config import DATASET, DEFAULT_SYNONYMS
from preprocessing.pos_tagger import TaggedToken
from utils.helpers import safe_load_json, sign_key


def load_synonyms() -> dict[str, str]:
    user_synonyms = safe_load_json(DATASET.synonyms, {})
    synonyms = dict(DEFAULT_SYNONYMS)
    if isinstance(user_synonyms, dict):
        for source, target in user_synonyms.items():
            synonyms[sign_key(str(source))] = sign_key(str(target))
    return synonyms


def map_synonyms(tagged_tokens: list[TaggedToken], synonyms: dict[str, str] | None = None) -> list[TaggedToken]:
    synonyms = synonyms if synonyms is not None else load_synonyms()
    return [TaggedToken(synonyms.get(token.text, token.text), token.pos) for token in tagged_tokens]
