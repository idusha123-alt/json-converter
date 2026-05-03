import json

def convert_oxford_to_json(input_filename="Oxford 5000.txt", output_filename="oxford_words.json"):
    levels = {
        "A1": [],
        "A2": [],
        "B1": [],
        "B2": [],
        "C1": [],
        "C2": []
    }
    
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
               
                parts = line.split()
                word = parts[0].lower().strip()
                
                
                level = "B1" 
                for part in parts[1:]:
                    if part.upper() in levels:
                        level = part.upper()
                        break
                
                if level in levels:
                    levels[level].append(word)
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(levels, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Success!")
        print(f"   Converted {sum(len(v) for v in levels.values())} words")
        print(f"   Saved as: {output_filename}")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{input_filename}' not found in the same folder.")
        print("Make sure the Oxford txt file is in the same directory as this Python script.")
    except Exception as e:
        print(f"❌ Error: {e}")

convert_oxford_to_json()
