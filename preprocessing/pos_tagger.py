from __future__ import annotations

from dataclasses import dataclass

from config import NEGATIONS, QUESTION_WORDS, TIME_WORDS


@dataclass(frozen=True)
class TaggedToken:
    text: str
    pos: str


_PRONOUNS = {"i", "me", "my", "you", "your", "he", "she", "we", "they", "their"}
_COMMON_VERBS = {
    "go",
    "come",
    "want",
    "need",
    "help",
    "understand",
    "know",
    "remember",
    "forget",
    "think",
    "hear",
    "listen",
    "talk",
    "speak",
    "tell",
    "ask",
    "answer",
    "say",
    "read",
    "write",
    "study",
    "learn",
    "teach",
    "work",
    "play",
    "watch",
    "walk",
    "run",
    "sit",
    "stand",
    "wait",
    "meet",
    "visit",
    "travel",
    "drive",
    "buy",
    "give",
    "take",
    "bring",
    "show",
    "call",
    "use",
    "make",
    "change",
    "choose",
    "join",
    "leave",
    "stay",
    "find",
    "lose",
    "finish",
    "stop",
    "start",
    "move",
    "open",
    "close",
    "drink",
    "eat",
    "cook",
    "pay",
    "sleep",
  }
_COMMON_ADJECTIVES = {
    "good",
    "bad",
    "happy",
    "sad",
    "angry",
    "scared",
    "tired",
    "hungry",
    "thirsty",
    "excited",
    "big",
    "small",
    "old",
    "young",
    "new",
    "hot",
    "cold",
    "easy",
    "difficult",
    "important",
    "beautiful",
    "dirty",
    "clean",
    "fast",
    "slow",
  }


def tag_tokens(tokens: list[str]) -> list[TaggedToken]:
    spacy_tags = _tag_with_spacy(tokens)
    if spacy_tags is not None:
        return spacy_tags
    return [_fallback_tag(token) for token in tokens]


def _tag_with_spacy(tokens: list[str]) -> list[TaggedToken] | None:
    try:
        import spacy

        nlp = spacy.load("en_core_web_sm")
    except Exception:
        return None

    doc = nlp(" ".join(tokens))
    return [TaggedToken(token.text.lower(), token.pos_) for token in doc]


def _fallback_tag(token: str) -> TaggedToken:
    if token.isdigit():
        return TaggedToken(token, "NUM")
    if token in QUESTION_WORDS:
        return TaggedToken(token, "WH")
    if token in TIME_WORDS:
        return TaggedToken(token, "TIME")
    if token in NEGATIONS:
        return TaggedToken(token, "NEG")
    if token in _PRONOUNS:
        return TaggedToken(token, "PRON")
    if token in _COMMON_VERBS or token.endswith("ing") or token.endswith("ed"):
        return TaggedToken(token, "VERB")
    if token in _COMMON_ADJECTIVES:
        return TaggedToken(token, "ADJ")
    return TaggedToken(token, "NOUN")
