from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class DatasetPaths:
    root: Path = BASE_DIR / "dataset"
    words: Path = BASE_DIR / "dataset" / "words"
    alphabets: Path = BASE_DIR / "dataset" / "alphabets"
    numbers: Path = BASE_DIR / "dataset" / "numbers"
    metadata: Path = BASE_DIR / "dataset" / "metadata"

    @property
    def sign_dictionary(self) -> Path:
        return self.metadata / "sign_dictionary.json"

    @property
    def alphabet_dictionary(self) -> Path:
        return self.metadata / "alphabet_dictionary.json"

    @property
    def number_dictionary(self) -> Path:
        return self.metadata / "number_dictionary.json"

    @property
    def stopwords(self) -> Path:
        return self.metadata / "stopwords.json"

    @property
    def synonyms(self) -> Path:
        return self.metadata / "synonyms.json"


DATASET = DatasetPaths()
OUTPUT_DIR = BASE_DIR / "assets" / "generated"
MERGED_VIDEO_PATH = OUTPUT_DIR / "asl_output.mp4"

QUESTION_WORDS = {"who", "what", "when", "where", "why", "how", "which"}
NEGATIONS = {"no", "not", "never", "cannot", "can't", "dont", "don't"}
TIME_WORDS = {
    "today",
    "tomorrow",
    "yesterday",
    "morning",
    "afternoon",
    "evening",
    "night",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "week",
    "month",
    "year",
    "now",
    "later",
    "soon",
}

DEFAULT_SYNONYMS = {
    "hey": "hello",
    "hi": "hello",
    "bye": "goodbye",
    "thanks": "thank you",
    "thankyou": "thank you",
    "physician": "doctor",
    "clinic": "hospital",
    "ill": "sick",
    "unwell": "sick",
    "nearest": "near",
    "nearby": "near",
    "automobile": "car",
    "purchase": "buy",
    "supper": "dinner",
    "cellphone": "phone",
    "mobile": "phone",
    "loudly": "loud",
    "rapid": "fast",
    "quick": "fast",
    "difficult": "difficult",
}

PHRASE_SIMPLIFICATIONS = {
    "nearest hospital": "hospital",
    "near hospital": "hospital",
    "nearby hospital": "hospital",
    "closest hospital": "hospital",
    "sign language": "sign language",
    "thank you": "thank you",
    "how are you": "you how",
    "what is your name": "name what",
    "where is": "where",
    "where are": "where",
}
