import json
import re

# Input file path and output file path
input_file = "frequency-list.txt.txt"
output_file = "frequency-list.json"

json_data = {}

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        # Split the line by pipe characters
        parts = [p.strip() for p in line.split("|") if p.strip()]

        if len(parts) >= 3:
            freq_num = parts[0]
            french_word = parts[1]
            english_word = parts[2]

            json_data[freq_num] = {
                "english": english_word,
                "french": french_word,
            }

# Save to JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("Conversion complete!")
