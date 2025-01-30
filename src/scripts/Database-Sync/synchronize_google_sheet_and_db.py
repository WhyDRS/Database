import os
import json
from google_sheet_utils import GoogleSheetHandler
from database_utils import DatabaseHandler

# Columns that are the source of truth from the DB (0-based indices):
SOURCE_OF_TRUTH_COLUMNS = [0, 1, 2, 18]

def main():
    # Load credentials and environment variables
    sheet_id = os.environ['SHEET_ID']
    creds_json = json.loads(os.environ['GOOGLE_API_KEYS'])
    db_file_path = 'data/Issuers/test.db'
    json_file_path = 'data/Issuers/test.json'

    # Initialize handlers
    db_handler = DatabaseHandler(db_file_path)
    sheet_handler = GoogleSheetHandler(sheet_id, creds_json, SOURCE_OF_TRUTH_COLUMNS)

    # Step 1: Read database data
    db_data = db_handler.read_database_data()

    # Step 2: Update the sheet from the DB for source-of-truth columns (case-insensitive matching)
    sheet_handler.update_google_sheet('test', db_data)

    # Step 3: Read the now-updated sheet data
    sheet_data = sheet_handler.read_sheet_data('test')

    # Step 4: Update the database from the sheet data (for non-source-of-truth columns)
    db_handler.update_database(sheet_data)

    # Step 5: Export the updated database to JSON
    db_handler.export_database_to_json(json_file_path)

    print("Synchronization between Google Sheet and database completed successfully.")


if __name__ == "__main__":
    main()
