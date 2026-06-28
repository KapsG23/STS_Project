from __future__ import annotations

import argparse

from pipeline import SpeechToASLPipeline


EXAMPLE_SENTENCES = [
    "Where is the nearest hospital?",
    "I need help today.",
    "Thank you doctor.",
    "I want water.",
]


def run_cli(text: str, merge: bool = False) -> None:
    result = SpeechToASLPipeline(merge_videos=merge).run_text(text)
    print(f"Speech/Text : {result.source_text}")
    print(f"ASL Gloss   : {result.gloss}")
    print("Assets:")
    for asset in result.assets:
        print(f"  - {asset.token:12} {asset.asset_type:5} {asset.path}")
    if result.merged_video:
        print(f"Merged video: {result.merged_video}")


def run_streamlit() -> None:
    import streamlit as st

    st.set_page_config(page_title="Speech to ASL", layout="wide")
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1120px;
        }
        .asset-label {
            font-size: 0.82rem;
            color: #475467;
            margin-bottom: 0.35rem;
        }
        .gloss-output code {
            font-size: 1.1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("Speech to ASL Converter")
    st.caption("English speech/text -> normalized ASL gloss -> dataset video/image retrieval")

    with st.sidebar:
        st.header("Pipeline")
        merge = st.checkbox("Merge available word videos", value=False)
        example = st.selectbox("Try an example", EXAMPLE_SENTENCES)
        st.markdown("Dataset sources: `dataset/words`, `dataset/alphabets`, `dataset/numbers`")

    text = st.text_area("Speech transcript or typed sentence", value=example, height=115)
    run = st.button("Convert to ASL", type="primary")

    if run and text.strip():
        result = SpeechToASLPipeline(merge_videos=merge).run_text(text)

        left, right = st.columns([1, 1], gap="large")
        with left:
            st.subheader("Recognized Speech/Text")
            st.write(result.source_text)

            st.subheader("Final ASL Gloss")
            st.markdown('<div class="gloss-output">', unsafe_allow_html=True)
            st.code(result.gloss or "(no gloss generated)", language="text")
            st.markdown("</div>", unsafe_allow_html=True)

            with st.expander("View pipeline tokens"):
                st.write(result.gloss_result.preprocessing.final_tokens)

        with right:
            st.subheader("Retrieved Signs")
            if not result.assets:
                st.warning("No assets matched. Add signs to the dataset or metadata dictionaries.")

            grid = st.columns(2, gap="medium")
            for index, asset in enumerate(result.assets):
                with grid[index % 2]:
                    st.markdown(
                        f'<div class="asset-label"><strong>{asset.token.upper()}</strong> - {asset.source}</div>',
                        unsafe_allow_html=True,
                    )
                    if asset.asset_type == "video":
                        st.video(str(asset.path))
                    else:
                        st.image(str(asset.path), width=170)

            if result.merged_video:
                st.subheader("Merged Sign Video")
                st.video(str(result.merged_video))


def main() -> None:
    parser = argparse.ArgumentParser(description="Speech/Text to ASL gloss and sign retrieval")
    parser.add_argument("--text", help="Sentence to convert. If omitted, launches Streamlit when available.")
    parser.add_argument("--merge", action="store_true", help="Merge matched word videos with MoviePy.")
    args = parser.parse_args()

    if args.text:
        run_cli(args.text, merge=args.merge)
        return

    try:
        run_streamlit()
    except ModuleNotFoundError:
        run_cli("Where is the nearest hospital?", merge=False)


if __name__ == "__main__":
    main()
