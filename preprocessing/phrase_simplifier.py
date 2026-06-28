from __future__ import annotations

from config import PHRASE_SIMPLIFICATIONS
from preprocessing.pos_tagger import TaggedToken
from utils.helpers import sign_key


def simplify_text_phrases(text: str) -> str:
    simplified = f" {sign_key(text)} "
    for phrase, replacement in sorted(PHRASE_SIMPLIFICATIONS.items(), key=lambda item: len(item[0]), reverse=True):
        simplified = simplified.replace(f" {phrase} ", f" {replacement} ")
    return " ".join(simplified.split())


def simplify_token_phrases(tagged_tokens: list[TaggedToken]) -> list[TaggedToken]:
    tokens = [token.text for token in tagged_tokens]
    output: list[TaggedToken] = []
    index = 0
    phrase_rules = [
        (phrase.split(), replacement)
        for phrase, replacement in sorted(PHRASE_SIMPLIFICATIONS.items(), key=lambda item: len(item[0]), reverse=True)
    ]

    while index < len(tokens):
        matched = False
        for phrase_tokens, replacement in phrase_rules:
            end = index + len(phrase_tokens)
            if tokens[index:end] == phrase_tokens:
                output.append(TaggedToken(replacement, tagged_tokens[index].pos))
                index = end
                matched = True
                break
        if not matched:
            output.append(tagged_tokens[index])
            index += 1

    return output
