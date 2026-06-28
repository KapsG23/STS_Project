from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from config import BASE_DIR


def safe_load_json(path: Path, default: Any) -> Any:
    if not path.exists() or path.stat().st_size == 0:
        return default
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default


def project_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return BASE_DIR / path


def sign_key(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"\s+", " ", value)
    return value


def dictionary_key(value: str) -> str:
    return sign_key(value).replace(" ", "_")


def unique_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item not in seen:
            output.append(item)
            seen.add(item)
    return output


def find_existing_path(path: Path) -> Path | None:
    if path.exists():
        return path

    parent = path.parent
    stem = path.stem
    suffix = path.suffix
    candidates = {
        parent / f"{stem.replace('_', ' ')}{suffix}",
        parent / f"{stem.replace(' ', '_')}{suffix}",
        parent / f"{stem.lower()}{suffix}",
        parent / f"{stem.upper()}{suffix}",
        parent / f"{stem.title()}{suffix}",
    }
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None
