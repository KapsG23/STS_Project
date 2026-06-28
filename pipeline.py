from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from grammar.gloss_converter import GlossResult, convert_to_gloss
from retrieval.merge_video import merge_video_assets
from retrieval.video_search import SignAsset, SignAssetRetriever


@dataclass(frozen=True)
class SpeechToASLResult:
    source_text: str
    gloss_result: GlossResult
    assets: list[SignAsset]
    merged_video: Path | None

    @property
    def gloss(self) -> str:
        return self.gloss_result.gloss


class SpeechToASLPipeline:
    def __init__(self, merge_videos: bool = False) -> None:
        self.retriever = SignAssetRetriever()
        self.merge_videos = merge_videos

    def run_text(self, text: str) -> SpeechToASLResult:
        gloss_result = convert_to_gloss(text)
        assets = self.retriever.retrieve_many(gloss_result.gloss_tokens)
        merged_video = merge_video_assets(assets) if self.merge_videos else None
        return SpeechToASLResult(
            source_text=text,
            gloss_result=gloss_result,
            assets=assets,
            merged_video=merged_video,
        )
