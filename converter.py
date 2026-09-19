import json
import re
import time
from deep_translator import GoogleTranslator

def convert_txt_to_json(input_txt_path, output_json_path):
    with open(input_txt_path, 'r', encoding='utf-8') as f:
        # Strip lines and ignore completely blank lines
        lines = [line.strip() for line in f if line.strip()]
        
    entries = []
    i = 0
    
    print("Beginning structural file parsing...")
    while i < len(lines):
        line = lines[i]
        
        # Check if the line is a frequency number (e.g., "50.", "2500.")
        if re.match(r'^\d+\.$', line):
            freq_number = int(line.rstrip('.'))
            
            # The line right after the number is always the French word
            i += 1
            if i < len(lines):
                french_word = lines[i]
                
                # Default configuration for a clean entry
                entry = {
                    "freqNumber": freq_number,
                    "word": french_word,
                    "engWord": ""
                }
                
                # Look ahead to see if an English word exists before the next number
                if i + 1 < len(lines) and not re.match(r'^\d+\.$', lines[i + 1]):
                    i += 1
                    entry["engWord"] = lines[i]
                    
                    # Look ahead again to skip part of speech lines if they exist
                    if i + 1 < len(lines) and not re.match(r'^\d+\.$', lines[i + 1]):
                        i += 1  # Skips the part of speech string safely
                        
                entries.append(entry)
        i += 1

    print(f"Parsing complete! Found {len(entries)} words in your text file.")
    print("Beginning safe high-speed batch translations...")
    
    # Isolate missing or broken translation indices
    missing_entries = [e for e in entries if not e["engWord"] or "[Error" in e["engWord"] or "[Translation" in e["engWord"]]
    
    batch_size = 50
    translator = GoogleTranslator(source='fr', target='en')
    
    for b in range(0, len(missing_entries), batch_size):
        chunk = missing_entries[b:b + batch_size]
        words_to_translate = [e["word"] for e in chunk]
        combined_text = "\n".join(words_to_translate)
        
        print(f"Translating batch {b//batch_size + 1} ({len(chunk)} words)...")
        
        success = False
        retries = 3
        while retries > 0 and not success:
            try:
                translated_block = translator.translate(combined_text)
                translated_words = [w.strip().lower() for w in translated_block.split("\n")]
                
                for index, item in enumerate(chunk):
                    if index < len(translated_words):
                        item["engWord"] = translated_words[index]
                    else:
                        item["engWord"] = "[Missing Data Match]"
                
                success = True
                time.sleep(2) # Safe rest interval
                
            except Exception as e:
                retries -= 1
                print(f"Server rate notice triggered. Resting 10 seconds... ({retries} left). Error: {e}")
                time.sleep(10)
        
        if not success:
            print("Batch threshold failed. Defaulting to single string mode for this block...")
            for item in chunk:
                try:
                    item["engWord"] = translator.translate(item["word"]).lower()
                    time.sleep(1.5)
                except:
                    item["engWord"] = "[Translation Error]"

    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(entries, json_file, ensure_ascii=False, indent=4)
        
    print(f"\n⚡ Success! Re-parsed full file and saved output to: {output_json_path}")

if __name__ == "__main__":
    convert_txt_to_json("list.txt", "french_frequency.json")
