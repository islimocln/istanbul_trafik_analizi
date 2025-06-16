import json
import os

INPUT = "restaurants_with_reviews.json"
OUTPUT = "restaurants_with_reviews_fixed.json"

with open(INPUT, "r", encoding="utf-8") as f:
    restaurants = json.load(f)

for restaurant in restaurants:
    if "photos" in restaurant:
        restaurant["photos"] = [
            "photos/" + os.path.basename(photo)
            for photo in restaurant["photos"]
        ]

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=2)

print(f"Düzenlenmiş dosya: {OUTPUT}") 