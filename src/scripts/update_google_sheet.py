import gspread
import pandas as pd
import os
import json
import sqlite3

# Load credentials from the environment variable
creds_json = json.loads(os.environ['GOOGLE_API_KEYS'])  # Parse JSON credentials from an environment variable

# Authenticate with the Google Sheets API
gc = gspread.service_account_from_dict(creds_json)  # Use credentials to authenticate and create a Google Sheets client

# Open the Google Sheet using the provided SHEET_ID
sheet = gc.open_by_key(os.environ['SHEET_ID'])  # Open the spreadsheet using the SHEET_ID from environment variables

# Select the worksheet to update
worksheet = sheet.worksheet("Full_Database_Backend")  # Specify the worksheet name within the spreadsheet to work with

# Connect to the SQLite database
db_file_path = 'data/Full_Database_Backend.db'  # Define the path to the database file
if not os.path.exists(db_file_path):
    raise FileNotFoundError(f"Database file not found: {db_file_path}")  # Raise an error if the database file does not exist
conn = sqlite3.connect(db_file_path)  # Open a connection to the SQLite database

# Read data from the database
query = "SELECT Ticker, Exchange, CompanyNameIssuer, CIK FROM full_database_backend"  # Adjusted to fetch only the required columns
df_db = pd.read_sql_query(query, conn)  # Execute the SQL query and store the results in a pandas DataFrame

# Replace NaN and infinite values with empty strings
df_db = df_db.replace([pd.NA, pd.NaT, float('inf'), -float('inf'), None], '', inplace=False).fillna('')

# Fetch current data from Google Sheet to find out the range to update
current_data = worksheet.get_all_values()
current_tickers = {row[0]: idx for idx, row in enumerate(current_data) if row[0]}  # Create a dictionary of current tickers and their row indices

# Prepare updates for specified columns and new rows to append
updates = []
new_rows = []
for index, row in df_db.iterrows():
    if row['Ticker'] in current_tickers:
        # Prepare the cell updates
        row_idx = current_tickers[row['Ticker']]
        updates.append(gspread.Cell(row_idx + 1, 1, row['Ticker']))  # Column 1: Ticker
        updates.append(gspread.Cell(row_idx + 1, 2, row['Exchange']))  # Column 2: Exchange
        updates.append(gspread.Cell(row_idx + 1, 3, row['CompanyNameIssuer']))  # Column 3: CompanyNameIssuer
        updates.append(gspread.Cell(row_idx + 1, 19, row['CIK']))  # Column 19: CIK
    else:
        # Append new row if ticker not found
        new_row = [row['Ticker'], row['Exchange'], row['CompanyNameIssuer']] + [''] * 15 + [row['CIK']] + [''] * (worksheet.col_count - 20)
        new_rows.append(new_row)

# Batch update the cells in Google Sheet
if updates:
    worksheet.update_cells(updates, value_input_option='USER_ENTERED')

# Append new rows to the Google Sheet
if new_rows:
    start_row = len(current_data) + 1  # Calculate starting row for new data
    worksheet.append_rows(new_rows, value_input_option='USER_ENTERED')
    # Set the background color for new rows to white
    end_row = start_row + len(new_rows) - 1
    range_format = f'A{start_row}:Z{end_row}'  # Adjust the column range as per your sheet's width
    worksheet.format(range_format, {
        "backgroundColor": {
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0  # Explicitly set to white
        }
    })

print("Selected columns in Google Sheet updated and new rows added successfully.")
