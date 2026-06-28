from __future__ import annotations

from dataclasses import dataclass

from preprocessing.lemmatizer import lemmatize_tokens
from preprocessing.ner import handle_named_entities
from preprocessing.normalize import normalize_text
from preprocessing.phrase_simplifier import simplify_text_phrases, simplify_token_phrases
from preprocessing.pos_tagger import TaggedToken, tag_tokens
from preprocessing.stopwords import remove_stopwords
from preprocessing.synonym_mapper import map_synonyms
from preprocessing.tokenizer import tokenize


@dataclass(frozen=True)
class PreprocessingResult:
    normalized_text: str
    tokens: list[str]
    tagged_tokens: list[TaggedToken]
    filtered_tokens: list[TaggedToken]
    final_tokens: list[str]


def preprocess_text(text: str) -> PreprocessingResult:
    normalized = normalize_text(text)
    simplified_text = simplify_text_phrases(normalized)
    tokens = tokenize(simplified_text)
    tagged = tag_tokens(tokens)
    filtered = remove_stopwords(tagged)
    lemmatized = lemmatize_tokens(filtered)
    entities = handle_named_entities(lemmatized)
    synonyms = map_synonyms(entities)
    simplified_tokens = simplify_token_phrases(synonyms)
    final_tokens = [token.text for token in simplified_tokens]
    return PreprocessingResult(
        normalized_text=normalized,
        tokens=tokens,
        tagged_tokens=tagged,
        filtered_tokens=filtered,
        final_tokens=final_tokens,
    )
