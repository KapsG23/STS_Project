from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from config import DATASET
from utils.helpers import dictionary_key, find_existing_path, project_path, safe_load_json, sign_key


@dataclass(frozen=True)
class SignAsset:
    token: str
    asset_type: str
    path: Path
    source: str


class SignAssetRetriever:
    def __init__(self) -> None:
        self.signs = safe_load_json(DATASET.sign_dictionary, {})
        self.alphabet = safe_load_json(DATASET.alphabet_dictionary, {})
        self.numbers = safe_load_json(DATASET.number_dictionary, {})

    def retrieve_many(self, gloss_tokens: list[str]) -> list[SignAsset]:
        assets: list[SignAsset] = []
        for token in gloss_tokens:
            assets.extend(self.retrieve_token(token))
        return assets

    def retrieve_token(self, token: str) -> list[SignAsset]:
        token = sign_key(token)
        word = self._word_asset(token)
        if word:
            return [word]

        if token.isdigit():
            return [asset for digit in token for asset in [self._number_asset(digit)] if asset]

        if len(token) == 1:
            letter = self._letter_asset(token)
            return [letter] if letter else []

        # Unknown words are fingerspelled so the demo always has visual output.
        spelled = [self._letter_asset(letter) for letter in token if letter.isalpha()]
        return [asset for asset in spelled if asset]

    def _word_asset(self, token: str) -> SignAsset | None:
        keys = [dictionary_key(token), sign_key(token), sign_key(token).replace("_", " ")]
        for key in keys:
            entry = self.signs.get(key)
            if isinstance(entry, dict) and "path" in entry:
                path = find_existing_path(project_path(entry["path"]))
                if path:
                    return SignAsset(token=token, asset_type="video", path=path, source="metadata")

        file_candidates = [
            DATASET.words / f"{token}.mp4",
            DATASET.words / f"{token.replace('_', ' ')}.mp4",
            DATASET.words / f"{token.replace(' ', '_')}.mp4",
        ]
        for candidate in file_candidates:
            path = find_existing_path(candidate)
            if path:
                return SignAsset(token=token, asset_type="video", path=path, source="filesystem")
        return None

    def _number_asset(self, digit: str) -> SignAsset | None:
        entry = self.numbers.get(digit)
        if not entry:
            return None
        path = find_existing_path(project_path(entry))
        if not path:
            return None
        return SignAsset(token=digit, asset_type="image", path=path, source="number")

    def _letter_asset(self, letter: str) -> SignAsset | None:
        entry = self.alphabet.get(letter.lower())
        if not entry:
            return None
        path = find_existing_path(project_path(entry))
        if not path:
            return None
        return SignAsset(token=letter.lower(), asset_type="image", path=path, source="alphabet")
