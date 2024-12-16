import requests
import os
import time

# URL for the SEC JSON data
SEC_JSON_URL = "https://www.sec.gov/files/company_tickers_exchange.json"

# Data folder and output file paths
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)
OUTPUT_FILE = os.path.join(DATA_FOLDER, "company_tickers_exchange.json")

# HTTP headers to mimic a browser and provide contact info
HEADERS = {
    "User-Agent": "MyAppName/1.0 (hi@WhyDRS.org)"
}

# Rate limit configuration
MAX_REQUESTS_PER_SECOND = 10
SLEEP_TIME = 1 / MAX_REQUESTS_PER_SECOND

def download_sec_data(url, headers, output_file):
    """Download the SEC JSON data and save it to a file."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error if the request failed
    with open(output_file, "wb") as file:
        file.write(response.content)
    print(f"SEC data file saved to {output_file}")

# Download the JSON data
download_sec_data(SEC_JSON_URL, HEADERS, OUTPUT_FILE)

# Sleep to respect rate limits
time.sleep(SLEEP_TIME)
