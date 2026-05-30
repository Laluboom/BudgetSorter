import requests
import json
import csv
import re
import os

# --- CONFIGURATION ---
API_KEY = 'helloworld' 
IMAGE_PATH = 'tesco_receipt.jpeg' 
CSV_FILENAME = 'receipt_log.csv'
JSON_CACHE_FILE = 'raw_ocr_debug.json' # Where we save the API output

# SET THIS TO TRUE to test your regex without calling the API
# SET THIS TO FALSE to process a new image
USE_LOCAL_CACHE = False 

def get_ocr_data(filename, api_key, cache_file):
    """
    Checks if we have local data. If yes, load it.
    If no, call the API and save the data for next time.
    """
    
    # 1. Try to load from local file first (Offline Mode)
    if USE_LOCAL_CACHE and os.path.exists(cache_file):
        print(f"DEBUG: Loading data from local file: {cache_file}")
        print("DEBUG: (No API call was made)")
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    # 2. If no local file or Cache is False, call the API (Online Mode)
    print("DEBUG: Calling OCR API...")
    payload = {
        'apikey': api_key,
        'language': 'eng',
        'isOverlayRequired': False,
        'OCREngine': '2', 
        'scale': 'true',
        'detectOrientation': 'true',
        'isTable': 'true'
    }
    
    with open(filename, 'rb') as f:
        r = requests.post(
            'https://api.ocr.space/parse/image',
            files={filename: f},
            data=payload,
        )
    
    result = r.json()

    # 3. Save the result to a file so we can reuse it later
    if result.get('OCRExitCode') == 1:
        print(f"DEBUG: API Success. Saving raw output to {cache_file}...")
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4) # indent=4 makes it readable for humans
    
    return result

def parse_receipt_data(text):
    """
    Your Regex Playground. Edit this function to improve accuracy.
    """
    lines = text.split('\r\n')
    
    # --- REGEX AREA: MODIFY THESE TO PERFECT YOUR MATCHING ---
    
    # Looks for dates like 12/11/25 or 2025-12-11
    date_pattern = re.compile(r'\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}') 
    
    # Looks for prices. \d{1,3} handles numbers like 1,000.00
    price_pattern = re.compile(r'(\d{1,3}(?:,\d{3})*\.\d{2})') 
    
    # ---------------------------------------------------------

    extracted_date = "Unknown Date"
    items_found = [] 
    grand_total = 0.0
    ignore_keywords = ['tax', 'subtotal', 'change', 'cash', 'visa', 'credit', 'balance', 'total']

    for line in lines:
        clean_line = line.strip()
        
        # Search for Date
        if extracted_date == "Unknown Date":
            date_match = date_pattern.search(clean_line)
            if date_match:
                extracted_date = date_match.group(0)

        # Search for Prices
        price_match = price_pattern.search(clean_line)
        if price_match:
            try:
                price_str = price_match.group(1).replace(',', '')
                price_val = float(price_str)
                lower_line = clean_line.lower()
                
                if 'total' in lower_line:
                    if price_val > grand_total:
                        grand_total = price_val
                
                elif not any(keyword in lower_line for keyword in ignore_keywords):
                    item_name = clean_line.replace(price_match.group(0), '').strip()
                    item_name = item_name.rstrip('$. ')
                    if len(item_name) > 1:
                        items_found.append((item_name, price_val))
            except ValueError:
                continue

    return extracted_date, items_found, grand_total

def log_to_csv(date, items, total, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Date', 'Items List', 'Total Items', 'Grand Total'])
        
        item_names = " | ".join([x[0] for x in items])
        writer.writerow([date, item_names, len(items), total])
    print(f"Data appended to {filename}")

# --- MAIN FLOW ---

# 1. Get Data (Either from API or Local File)
data_json = get_ocr_data(IMAGE_PATH, API_KEY, JSON_CACHE_FILE)

# 2. Extract the text string from the JSON structure
if data_json.get('OCRExitCode') == 1:
    raw_text = data_json['ParsedResults'][0]['ParsedText']
    
    # Print raw text so you can see what you are working with
    print("\n--- RAW TEXT FROM JSON ---")
    print(raw_text)
    print("--------------------------\n")

    # 3. Run the parsing logic
    r_date, r_items, r_total = parse_receipt_data(raw_text)
    
    print(f"Date Found: {r_date}")
    print(f"Items Found: {len(r_items)}")
    print(f"Total Found: {r_total}")
    
    # 4. Save to CSV
    log_to_csv(r_date, r_items, r_total, CSV_FILENAME)

else:
    print("Error in processing:", data_json.get('ErrorMessage'))