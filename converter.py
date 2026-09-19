import json
import re
from deep_translator import GoogleTranslator

def convert_txt_to_json(input_txt_path, output_json_path):
    with open(input_txt_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
        
    entries = []
    current_entry = {}
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if re.match(r'^\d+\.$', line):
            if current_entry:
                entries.append(current_entry)
                
            freq_number = int(line.rstrip('.'))
            current_entry = {
                "freqNumber": freq_number,
                "word": "",
                "engWord": ""
            }
            
            i += 1
            if i < len(lines):
                current_entry["word"] = lines[i]
                
            i += 1
            if i < len(lines) and not re.match(r'^\d+\.$', lines[i]):
                current_entry["engWord"] = lines[i]
                i += 1
                if i < len(lines) and not re.match(r'^\d+\.$', lines[i]):
                    i += 1
            continue
        else:
            i += 1
            
    if current_entry:
        entries.append(current_entry)

    print("Parsing text structure finished. Beginning rapid translations...")
    
    # Initialize the fast local translator object
    translator = GoogleTranslator(source='fr', target='en')
    
    for entry in entries:
        # Check if the word needs translation or contains an error string
        if not entry["engWord"] or "[Error:" in entry["engWord"]:
            french_word = entry["word"]
            print(f"Translating: {french_word} (#{entry['freqNumber']})")
            try:
                # Fast translation execution loop without manual sleep timers
                entry["engWord"] = translator.translate(french_word).lower()
            except Exception as e:
                entry["engWord"] = f"[Translation Failure: {str(e)}]"

    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(entries, json_file, ensure_ascii=False, indent=4)
        
    print(f"\nSuccess! File successfully saved to: {output_json_path}")

if __name__ == "__main__":
    convert_txt_to_json("list.txt", "french_frequency.json")

