import json
import ast
import os

def extract_linetexts(file_path):
    # 1. Check file existence
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # 2. Robust Loading (Handles both standard JSON and Python-style dicts)
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_data = f.read().strip()
        
    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError:
        try:
            # Fallback for single-quoted files
            data = ast.literal_eval(raw_data)
        except Exception:
            print("Error: Could not parse JSON file.")
            return

    # 3. Drill down to the Lines
    try:
        # Navigate the OCR.Space structure
        lines = data['ParsedResults_3'][0]['TextOverlay']['Lines']
        
        # Extract 'LineText' from each entry
        text_list = [line.get('LineText', '') for line in lines]
        
        # 4. Join them with a space
        combined_text = " ".join(text_list)
        
        return text_list, combined_text

    except (KeyError, IndexError, TypeError) as e:
        print(f"Structure Error: The JSON doesn't match standard OCR.Space format. ({e})")
        return [], ""

# --- USAGE ---
json_file = "OCR_parse/Tesco_OCR.json" # Change this to your filename

# Run extraction
raw_list, spaced_text = extract_linetexts(json_file)

if spaced_text:
    print("--- Option 1: As a Python List ---")
    print(raw_list)
    print("\n" + "="*30 + "\n")
    
    print("--- Option 2: All text with space in between ---")
    print(spaced_text)