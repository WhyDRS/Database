import os
import json
from google_sheet_utils import GoogleSheetHandler
from database_utils import DatabaseHandler

def main():
    # Load credentials and environment variables
    sheet_id = os.environ['SHEET_ID']
    creds_json = json.loads(os.environ['GOOGLE_API_KEYS'])
    db_file_path = 'data/Full_Database_Backend.db'
    json_file_path = 'data/Full_Database_Backend.json'

    # Initialize handlers
    sheet_handler = GoogleSheetHandler(sheet_id, creds_json)
    db_handler = DatabaseHandler(db_file_path)

    # Read data from Google Sheet
    data = sheet_handler.read_sheet_data('Full_Database_Backend')

    # Update database with data from Google Sheet
    db_handler.update_database(data)

    # Read data from database to find missing values for the Google Sheet
    db_data = db_handler.read_database_data()

    # Update Google Sheet with missing data from database
    sheet_handler.update_google_sheet('Full_Database_Backend', db_data)

    # Export database to JSON
    db_handler.export_database_to_json(json_file_path)

    print("Synchronization between Google Sheet and database completed successfully.")

if __name__ == "__main__":
    main()
