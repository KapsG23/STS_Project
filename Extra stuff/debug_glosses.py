# import json

# with open("WLASL_v0.3.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# print("Total glosses:", len(data))

# print("\nFirst 200 glosses:\n")

# for entry in data[:200]:
#     print(entry["gloss"])

# import json

# with open("WLASL_v0.3.json","r",encoding="utf-8") as f:
#     data=json.load(f)

# for entry in data:
#     if entry["gloss"] in [
#         "hello",
#         "help",
#         "thank",
#         "friend",
#         "computer",
#         "need",
#         "want",
#         "water",
#         "doctor"
#     ]:
#         print(entry["gloss"])

import json

with open("WLASL_v0.3.json","r",encoding="utf-8") as f:
    data=json.load(f)

for entry in data[:50]:
    print(entry["gloss"])