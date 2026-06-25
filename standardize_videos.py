from moviepy import VideoFileClip
import os

INPUT_FOLDER = "dataset/words"
OUTPUT_FOLDER = "dataset/words_standardized"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for filename in os.listdir(INPUT_FOLDER):

    if not filename.endswith(".mp4"):
        continue

    input_path = os.path.join(
        INPUT_FOLDER,
        filename
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    try:

        clip = VideoFileClip(input_path)

        clip = clip.resized(
            (224, 224)
        )

        clip.write_videofile(
            output_path,
            codec="libx264",
            fps=30,
            audio=False,
            logger=None
        )

        clip.close()

        print(
            f"Done: {filename}"
        )

    except Exception as e:

        print(
            f"Failed: {filename}"
        )

        print(e)