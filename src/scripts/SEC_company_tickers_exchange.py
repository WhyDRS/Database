import requests
import os
import time

# URL of the JSON file
url = "https://www.sec.gov/files/company_tickers_exchange.json"

# Path to the data folder
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

# Path to the output file
output_file = os.path.join(data_folder, "company_tickers_exchange.json")

# Set headers to mimic a browser request responsibly
headers = {
    "User-Agent": "MyAppName/1.0 (hi@WhyDRS.org)"
}

# Rate limit parameters
max_requests_per_second = 10
sleep_time = 1 / max_requests_per_second

# Function to download the JSON file
def download_file(url, headers, output_file):
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check that the request was successful
    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"File saved to {output_file}")

# Download the JSON file
download_file(url, headers, output_file)

# Sleep to respect rate limit
time.sleep(sleep_time)
