from __future__ import annotations

import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class STTResult:
    text: str
    engine: str


class MoonshineSTT:
    """Thin wrapper around moonshine-voice.

    Moonshine's microphone transcriber is interactive, so this class keeps it
    isolated from the core ASL pipeline. Use it when the dependency is installed
    and a microphone demo is needed.
    """

    def transcribe_microphone(self, language: str = "en") -> STTResult:
        command = [
            "python",
            "-m",
            "moonshine_voice.mic_transcriber",
            "--language",
            language,
        ]
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        text = (completed.stdout or "").strip()
        if completed.returncode != 0:
            raise RuntimeError((completed.stderr or "Moonshine transcription failed").strip())
        return STTResult(text=text, engine="moonshine")
