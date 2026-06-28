from __future__ import annotations

import json
import wave
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VoskConfig:
    model_path: Path


class VoskSTT:
    def __init__(self, config: VoskConfig) -> None:
        self.config = config

    def transcribe_wav(self, wav_path: Path) -> str:
        try:
            from vosk import KaldiRecognizer, Model
        except Exception as exc:
            raise RuntimeError("Install vosk and download a Vosk English model first.") from exc

        model = Model(str(self.config.model_path))
        with wave.open(str(wav_path), "rb") as source:
            recognizer = KaldiRecognizer(model, source.getframerate())
            chunks: list[str] = []
            while True:
                data = source.readframes(4000)
                if not data:
                    break
                if recognizer.AcceptWaveform(data):
                    chunks.append(json.loads(recognizer.Result()).get("text", ""))
            chunks.append(json.loads(recognizer.FinalResult()).get("text", ""))
        return " ".join(chunk for chunk in chunks if chunk).strip()
