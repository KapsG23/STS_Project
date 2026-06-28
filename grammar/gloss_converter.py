from __future__ import annotations

from dataclasses import dataclass

from grammar.asl_rules import apply_asl_order, tokens_to_gloss
from preprocessing.pipeline import PreprocessingResult, preprocess_text


@dataclass(frozen=True)
class GlossResult:
    source_text: str
    preprocessing: PreprocessingResult
    gloss_tokens: list[str]
    gloss: str


def convert_to_gloss(text: str) -> GlossResult:
    preprocessing = preprocess_text(text)
    gloss_tokens = apply_asl_order(preprocessing.final_tokens)
    return GlossResult(
        source_text=text,
        preprocessing=preprocessing,
        gloss_tokens=gloss_tokens,
        gloss=tokens_to_gloss(gloss_tokens),
    )
