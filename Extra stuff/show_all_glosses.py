import json

with open("WLASL_v0.3.json","r",encoding="utf-8") as f:
    data=json.load(f)

with open("all_glosses.txt","w",encoding="utf-8") as f:
    for entry in data:
        f.write(entry["gloss"] + "\n")

print("Done")