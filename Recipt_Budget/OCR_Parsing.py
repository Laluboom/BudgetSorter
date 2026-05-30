import requests
import json
import csv
import re
import os
from datetime import datetime

API_KEY = 'helloworld'  # Replace with your OCR.space API key from the environment for real use.
CSV_FILENAME = 'receipt_log.csv'
IMAGE_PATH = ['City_Sport_Receipt(1).jpeg',
              'Sainsbury(1).jpeg',
              'Tesco_receipt(1).jpeg']

def get_ocr_text(filename, api_key):
    """Sends image to OCR.space and returns the raw parsed text."""
    payload = {
        'apikey': api_key,
        'language': 'eng',
        'isOverlayRequired': False,
        'OCREngine': '2', # Optimized for receipts/broken text
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
    
    if result.get('OCRExitCode') == 1:
        print(result)
        return result['ParsedResults'][0]['ParsedText']
    else:
        print(f"Error: {result.get('ErrorMessage')}")
        return None

def parse_receipt_data(text):
    """
    Analyzes raw text to find Date, Items, and Total.
    Logic:
    1. Dates look like numbers with slashes/dashes.
    2. Prices look like decimals.
    3. If a line has a price but isn't 'Total'/'Tax', it's likely an item.
    """
    lines = text.split('\r\n')
    
    # 1. Regex Patterns
    # Matches: 12/11/2025, 12-11-25, 2025.12.11
    date_pattern = re.compile(r'\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}') 
    # Matches: 10.99, 1,000.00 (looks for decimal at end of line)
    price_pattern = re.compile(r'(\d{1,3}(?:,\d{3})*\.\d{2})') 

    extracted_date = "Unknown Date"
    items_found = [] # List of (Item Name, Price)
    grand_total = 0.0

    # Keywords to ignore when looking for items (so we don't list 'Tax' as an item)
    ignore_keywords = ['tax', 'subtotal', 'change', 'cash', 'visa', 'credit', 'balance', 'total']

    for line in lines:
        clean_line = line.strip()
        
        # --- A. FIND DATE ---
        if extracted_date == "Unknown Date":
            date_match = date_pattern.search(clean_line)
            if date_match:
                extracted_date = date_match.group(0)

        # --- B. FIND PRICES ---
        price_match = price_pattern.search(clean_line)
        
        if price_match:
            try:
                # Get the number (remove commas for float conversion)
                price_str = price_match.group(1).replace(',', '')
                price_val = float(price_str)
                
                # Check if this line is an Item or a Summary (Total/Tax)
                lower_line = clean_line.lower()
                
                # If the line contains "Total", assume it's the Grand Total
                if 'total' in lower_line:
                    # We usually want the largest 'Total' found on the page
                    if price_val > grand_total:
                        grand_total = price_val
                
                # If it doesn't contain tax/total/change, assume it's an ITEM
                elif not any(keyword in lower_line for keyword in ignore_keywords):
                    # Clean the text: Remove the price from the string to get Item Name
                    item_name = clean_line.replace(price_match.group(0), '').strip()
                    # Remove trailing symbols like $ or dots
                    item_name = item_name.rstrip('$. ')
                    
                    if len(item_name) > 1: # Ignore garbage noise
                        items_found.append((item_name, price_val))
            except ValueError:
                continue

    return extracted_date, items_found, grand_total

def log_to_csv(date, items, total, filename):
    """Saves the data to a CSV file."""
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write Header if new file
        if not file_exists:
            writer.writerow(['Date', 'Item Name', 'Item Price', 'Receipt Total', 'Total Items Count'])
        
        # Log: One row per receipt? Or one row per item?
        # Here we log a summary row for the whole receipt
        item_names = " | ".join([x[0] for x in items])
        item_count = len(items)
        
        writer.writerow([date, item_names, "VARIES", total, item_count])
        
        # OPTIONAL: If you want one row per ITEM instead, uncomment below:
        # for item_name, item_price in items:
        #     writer.writerow([date, item_name, item_price, total, item_count])

    print(f"Success! Saved to {filename}")

print("Scanning image...")
for image in IMAGE_PATH:
    raw_text = get_ocr_text(image, API_KEY)
    if raw_text:
        print("Parsing data...")
        r_date, r_items, r_total = parse_receipt_data(raw_text)
        
        print("-" * 30)
        print(f"Date: {r_date}")
        print(f"Total Cost: {r_total}")
        print(f"Items Found: {len(r_items)}")
        print("-" * 30)
        
        log_to_csv(r_date, r_items, r_total, CSV_FILENAME)
