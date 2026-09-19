import json
import re
import time
import requests

def convert_txt_to_json(input_txt_path, output_json_path):
    # Read and clean lines from the text file
    with open(input_txt_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
        
    entries = []
    current_entry = {}
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Identify the start of a new block (e.g., "1.", "2.", "80.")
        if re.match(r'^\d+\.$', line):
            if current_entry:
                entries.append(current_entry)
                
            freq_number = int(line.rstrip('.'))
            current_entry = {
                "freqNumber": freq_number,
                "word": "",
                "engWord": ""
            }
            
            # Line immediately after the number is always the French word
            i += 1
            if i < len(lines):
                current_entry["word"] = lines[i]
                
            # Check if an English word exists before the next frequency number
            i += 1
            if i < len(lines) and not re.match(r'^\d+\.$', lines[i]):
                current_entry["engWord"] = lines[i]
                i += 1
                
                # Skip the part of speech line if present
                if i < len(lines) and not re.match(r'^\d+\.$', lines[i]):
                    i += 1
            continue
        else:
            i += 1
            
    # Append the last processed entry
    if current_entry:
        entries.append(current_entry)

    # Fetch missing translations for entries past word 70-80
    print("Parsing complete. Fetching missing English words from free translation API...")
    for entry in entries:
        if not entry["engWord"]:
            french_word = entry["word"]
            print(f"Fetching English translation for: '{french_word}' (Rank {entry['freqNumber']})")
            
            # Using MyMemory Free Translation API for clean fr->en conversion
            api_url = f"https://translated.net{french_word}&langpair=fr|en"
            
            try:
                response = requests.get(api_url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    translation = data.get("responseData", {}).get("translatedText", "")
                    # Clean up translation output
                    entry["engWord"] = translation.strip().lower()
                else:
                    entry["engWord"] = "[Translation Error]"
            except Exception as e:
                entry["engWord"] = f"[Error: {str(e)}]"
                
            # 1-second delay to respect the free API rate limit
            time.sleep(1)

    # Save finalized list to a structured JSON file
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(entries, json_file, ensure_ascii=False, indent=4)
        
    print(f"\nSuccess! File successfully saved to: {output_json_path}")

# Run the script
if __name__ == "__main__":
    # Replace these paths with your actual filenames
    convert_txt_to_json("french_words.txt", "french_frequency.json")
