import json
import os
import shutil

# =========================
# PATHS
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JSON_FILE = os.path.join(BASE_DIR, "WLASL_v0.3.json")
VIDEOS_FOLDER = os.path.join(BASE_DIR, "videos")
TARGET_WORDS_FILE = os.path.join(BASE_DIR, "target_words.txt")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "dataset", "words")

# =========================
# LOAD JSON
# =========================

print("Loading WLASL JSON...")

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# =========================
# LOAD TARGET WORDS
# =========================

print("Loading target words...")

with open(TARGET_WORDS_FILE, "r", encoding="utf-8") as f:
    target_words = {
        line.strip().lower()
        for line in f
        if line.strip()
    }

print(f"Target words loaded: {len(target_words)}")

# =========================
# CREATE OUTPUT FOLDER
# =========================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Clear old extracted files
for file in os.listdir(OUTPUT_FOLDER):
    if file.endswith(".mp4"):
        os.remove(os.path.join(OUTPUT_FOLDER, file))

# =========================
# EXTRACTION
# =========================

copied = 0
missing_words = set()
found_words = set()

for entry in data:

    gloss = entry["gloss"].lower()

    if gloss not in target_words:
        continue

    found_words.add(gloss)

    video_found = False

    for instance in entry["instances"]:

        video_id = instance["video_id"]

        source_file = os.path.join(
            VIDEOS_FOLDER,
            f"{video_id}.mp4"
        )

        if os.path.exists(source_file):

            target_file = os.path.join(
                OUTPUT_FOLDER,
                f"{gloss}.mp4"
            )

            shutil.copy2(
                source_file,
                target_file
            )

            copied += 1

            video_found = True

            print(
                f"[COPIED] {gloss} -> {video_id}.mp4"
            )

            break

    if not video_found:
        missing_words.add(gloss)

# =========================
# REPORT
# =========================

not_found_in_wlasl = target_words - found_words

print("\n==============================")
print("EXTRACTION COMPLETE")
print("==============================")

print(f"Videos copied      : {copied}")
print(f"Words found        : {len(found_words)}")
print(f"Missing video file : {len(missing_words)}")
print(f"Not in WLASL       : {len(not_found_in_wlasl)}")

# Save reports

with open("found_words.txt", "w", encoding="utf-8") as f:
    for word in sorted(found_words):
        f.write(word + "\n")

with open("missing_words.txt", "w", encoding="utf-8") as f:
    for word in sorted(missing_words):
        f.write(word + "\n")

with open("not_in_wlasl.txt", "w", encoding="utf-8") as f:
    for word in sorted(not_found_in_wlasl):
        f.write(word + "\n")

print("\nGenerated:")
print("found_words.txt")
print("missing_words.txt")
print("not_in_wlasl.txt")