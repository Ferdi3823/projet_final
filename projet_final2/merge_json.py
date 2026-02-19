import json

merged = []
seen_ids = set()

for filename in ["data1.json", "data2.json"]:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

        for item in data:
            if item["id"] not in seen_ids:
                merged.append(item)
                seen_ids.add(item["id"])

# Sauvegarde finale
with open("merged.json", "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=4, ensure_ascii=False)

print("Fusion JSON terminée")
