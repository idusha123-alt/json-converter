import csv
import json

# File paths
input_file = "apera-french-top-1000.csv"
output_file = "apera-french-top-1000.json"

json_data = {}

with open(input_file, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)  # Automatically uses the first line as headers
    for row in reader:
        rank = row["rank"].strip()
        french_word = row["word"].strip()
        english_meaning = row["meaning"].strip()

        json_data[rank] = {
            "english": english_meaning,
            "french": french_word,
        }

# Save to JSON
with open(output_file, mode="w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("CSV to JSON conversion complete!")
