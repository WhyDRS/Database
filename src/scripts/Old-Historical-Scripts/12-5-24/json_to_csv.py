import pandas as pd
import os
import json

# Path to the JSON file
json_file_path = 'data/company_tickers_exchange.json'
csv_file_path = 'data/company_tickers_exchange.csv'

# Read the JSON file
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Extract fields and data
fields = data['fields']
records = data['data']

# Convert to DataFrame
df = pd.DataFrame(records, columns=fields)

# Save DataFrame to CSV
df.to_csv(csv_file_path, index=False)

print(f"CSV file saved to {csv_file_path}")
