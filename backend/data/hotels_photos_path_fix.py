import json
import os

INPUT = "hotels_with_reviews.json"
OUTPUT = "hotels_with_reviews_fixed.json"

with open(INPUT, "r", encoding="utf-8") as f:
    hotels = json.load(f)

for hotel in hotels:
    if "photos" in hotel:
        hotel["photos"] = [
            "photos/" + os.path.basename(photo)
            for photo in hotel["photos"]
        ]

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(hotels, f, ensure_ascii=False, indent=2)

print(f"Düzenlenmiş dosya: {OUTPUT}") 