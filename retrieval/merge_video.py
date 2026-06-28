from __future__ import annotations

from pathlib import Path

from config import MERGED_VIDEO_PATH
from retrieval.video_search import SignAsset


def merge_video_assets(assets: list[SignAsset], output_path: Path = MERGED_VIDEO_PATH) -> Path | None:
    videos = [asset.path for asset in assets if asset.asset_type == "video"]
    if not videos:
        return None

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from moviepy import VideoFileClip, concatenate_videoclips
    except Exception:
        try:
            from moviepy.editor import VideoFileClip, concatenate_videoclips
        except Exception:
            return None

    clips = []
    try:
        for path in videos:
            clips.append(VideoFileClip(str(path)))
        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile(str(output_path), codec="libx264", audio=False, logger=None)
        final.close()
        return output_path
    finally:
        for clip in clips:
            try:
                clip.close()
            except Exception:
                pass
