import os
import json
from csv_utils import MultipleCSVHandler
from database_utils import DatabaseHandler

# Columns that are the source of truth from the DB (0-based indices):
SOURCE_OF_TRUTH_COLUMNS = [0, 1, 2, 18]

def main():
    # Load environment variables if any
    db_file_path = 'data/Issuers/Main_Database.db'
    csv_dir_path = 'data/Issuers/Main-Database-CSV-Files'
    json_file_path = 'data/Issuers/Main_Database.json'

    # Initialize handlers
    db_handler = DatabaseHandler(db_file_path)
    multiple_csv_handler = MultipleCSVHandler(csv_dir_path, SOURCE_OF_TRUTH_COLUMNS)

    # Step 1: Read database data
    db_data = db_handler.read_database_data()

    # Step 2: Update the multiple CSV files from the DB for source-of-truth columns
    multiple_csv_handler.update_csv(db_data)

    # Step 3: Read the now-updated CSV data from all letter files
    csv_data = multiple_csv_handler.read_csv_data()

    # Step 4: Update the database from the CSV data (for non-source-of-truth columns)
    db_handler.update_database(csv_data)

    # Step 5: Export the updated database to JSON
    db_handler.export_database_to_json(json_file_path)

    print("Synchronization between CSV files and database completed successfully.")


if __name__ == "__main__":
    main() 