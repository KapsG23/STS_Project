from __future__ import annotations

from preprocessing.pos_tagger import TaggedToken


IRREGULAR = {
    "went": "go",
    "gone": "go",
    "came": "come",
    "bought": "buy",
    "gave": "give",
    "taken": "take",
    "took": "take",
    "children": "child",
    "people": "people",
    "men": "man",
    "women": "woman",
    "better": "good",
    "worse": "bad",
  }


def lemmatize_tokens(tagged_tokens: list[TaggedToken]) -> list[TaggedToken]:
    spacy_tokens = _lemmatize_with_spacy(tagged_tokens)
    if spacy_tokens is not None:
        return spacy_tokens

    output: list[TaggedToken] = []
    for token in tagged_tokens:
        lemma = _fallback_lemma(token.text, token.pos)
        output.append(TaggedToken(lemma, token.pos))
    return output


def _lemmatize_with_spacy(tagged_tokens: list[TaggedToken]) -> list[TaggedToken] | None:
    try:
        import spacy

        nlp = spacy.load("en_core_web_sm")
    except Exception:
        return None

    doc = nlp(" ".join(token.text for token in tagged_tokens))
    return [TaggedToken(token.lemma_.lower(), source.pos) for token, source in zip(doc, tagged_tokens)]


def _fallback_lemma(text: str, pos: str) -> str:
    if text in IRREGULAR:
        return IRREGULAR[text]
    if pos == "VERB":
        if text.endswith("ing") and len(text) > 5:
            return text[:-3]
        if text.endswith("ed") and len(text) > 4:
            return text[:-2]
    if pos == "NOUN" and text.endswith("s") and len(text) > 3:
        return text[:-1]
    return text
