from __future__ import annotations

import re


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("can't", "cannot")
    text = text.replace("n't", " not")
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
