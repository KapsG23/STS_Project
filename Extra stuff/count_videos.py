import os

files = os.listdir("videos")

print("Total videos:", len(files))

print("\nFirst 20 files:")

for file in sorted(files)[:20]:
    print(file)

print("\nLast 20 files:")

for file in sorted(files)[-20:]:
    print(file)