from __future__ import annotations

from preprocessing.pos_tagger import TaggedToken


NUMBER_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def handle_named_entities(tagged_tokens: list[TaggedToken]) -> list[TaggedToken]:
    output: list[TaggedToken] = []
    for token in tagged_tokens:
        if token.text in NUMBER_WORDS:
            output.append(TaggedToken(NUMBER_WORDS[token.text], "NUM"))
        else:
            output.append(token)
    return output
