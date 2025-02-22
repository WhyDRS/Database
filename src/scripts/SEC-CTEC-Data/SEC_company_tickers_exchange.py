import requests
import os
import time
import json

# URL for the SEC JSON data
SEC_JSON_URL = "https://www.sec.gov/files/company_tickers_exchange.json"

# Data folder and output file paths
DATA_FOLDER = "data/SEC-CTEC-Data"
os.makedirs(DATA_FOLDER, exist_ok=True)
OUTPUT_FILE = os.path.join(DATA_FOLDER, "company_tickers_exchange.json")

# HTTP headers to mimic a browser and provide contact info
HEADERS = {
    "User-Agent": "MyAppName/1.0 (hi@WhyDRS.org)"
}

# Rate limit configuration
MAX_REQUESTS_PER_SECOND = 10
SLEEP_TIME = 1 / MAX_REQUESTS_PER_SECOND

def download_and_process_sec_data(url, headers, output_file):
    """Download the SEC JSON data, process it, and save it."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Parse the JSON data
    json_data = response.json()
    fields = json_data['fields']
    data = json_data['data']
    
    # Process each entry to strip whitespace from CIK and Ticker
    processed_data = []
    for entry in data:
        processed_entry = entry.copy()
        processed_entry[0] = str(processed_entry[0]).strip()  # CIK
        processed_entry[2] = str(processed_entry[2]).strip()  # Ticker
        processed_data.append(processed_entry)
    
    # Save the processed data with both fields and data
    output_json = {
        "fields": fields,
        "data": processed_data
    }
    
    with open(output_file, "w") as file:
        json.dump(output_json, file, indent=4)
    print(f"Processed SEC data file saved to {output_file}")

# Download and process the JSON data
download_and_process_sec_data(SEC_JSON_URL, HEADERS, OUTPUT_FILE)

# Sleep to respect rate limits
time.sleep(SLEEP_TIME)
