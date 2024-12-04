import os
import json
from google_sheet_utils import GoogleSheetHandler
from database_utils import DatabaseHandler
from data_merger import DataMerger

def main():
    # Load credentials and environment variables
    sheet_id = os.environ['SHEET_ID']
    creds_json = json.loads(os.environ['GOOGLE_API_KEYS'])
    db_file_path = 'data/Full_Database_Backend.db'
    json_file_path = 'data/Full_Database_Backend.json'

    # Initialize handlers
    sheet_handler = GoogleSheetHandler(sheet_id, creds_json)
    db_handler = DatabaseHandler(db_file_path)
    data_merger = DataMerger()

    # Read data from sources
    df_sheet = sheet_handler.read_sheet_to_dataframe('Full_Database_Backend')
    df_db = db_handler.read_database_to_dataframe()

    # Merge data
    df_db_updates, df_sheet_updates = data_merger.merge_dataframes(df_sheet, df_db)

    # Apply updates
    db_handler.update_database(df_db_updates)
    sheet_handler.update_google_sheet('Full_Database_Backend', df_sheet_updates)

    # Export database to JSON
    db_handler.export_database_to_json(json_file_path)

    print("Synchronization between Google Sheet and database completed successfully.")

if __name__ == "__main__":
    main()
