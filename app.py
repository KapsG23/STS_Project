from __future__ import annotations

import argparse

from pipeline import SpeechToASLPipeline


def run_cli(text: str, merge: bool = False) -> None:
    result = SpeechToASLPipeline(merge_videos=merge).run_text(text)
    print(f"Speech/Text : {result.source_text}")
    print(f"ASL Gloss   : {result.gloss}")
    print("Assets:")
    for asset in result.assets:
        print(f"  - {asset.token:12} {asset.asset_type:5} {asset.path}")
    if result.merged_video:
        print(f"Merged video: {result.merged_video}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Speech/Text to ASL gloss and sign retrieval")
    parser.add_argument("--text", required=True, help="Sentence to convert.")
    parser.add_argument("--merge", action="store_true", help="Merge matched word videos with MoviePy.")
    args = parser.parse_args()

    run_cli(args.text, merge=args.merge)


if __name__ == "__main__":
    main()
