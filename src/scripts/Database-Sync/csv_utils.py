import csv
import os
import string

class CSVHandler:
    def __init__(self, csv_file_path, source_of_truth_columns):
        self.csv_file_path = csv_file_path
        self.source_of_truth_columns = source_of_truth_columns
        # Ensure CSV directory exists
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        
        # Create the file with headers if it doesn't exist
        if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0:
            self._initialize_csv_with_headers()

    def _initialize_csv_with_headers(self):
        # Define headers similar to the database structure
        headers = [
            "Ticker", "Exchange", "Company_Name_Issuer", "Transfer_Agent", "Online_Purchase",
            "DTC_Member_Number", "TA_URL", "Transfer_Agent_Pct", "IR_Emails", "IR_Phone_Number",
            "IR_Company_Address", "IR_URL", "IR_Contact_Info", "Shares_Outstanding", "CUSIP",
            "Company_Info_URL", "Company_Info", "Full_Progress_Pct", "CIK", "DRS",
            "Percent_Shares_DRSd", "Submission_Received", "Timestamps_UTC", "Learn_More_About_DRS",
            "Certificates_Offered", "S_And_P_500", "Incorporated_In"
        ]
        
        with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

    def read_csv_data(self):
        if not os.path.exists(self.csv_file_path):
            return []
            
        with open(self.csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            if not data:
                return []
            # Skip the header row
            return data[1:]

    def update_csv(self, db_data):
        # Read existing CSV data
        existing_data = self.read_csv_data()
        
        # Create a mapping from lowercase (CIK, Ticker, CompanyNameIssuer) to row
        key_to_row = {}
        for row in existing_data:
            # Ensure row has at least 19 elements to access CIK
            row = row + [''] * (27 - len(row))
            CIK = row[18].strip() if row[18] else ''
            Ticker = row[0].strip() if row[0] else ''
            CompanyNameIssuer = row[2].strip() if row[2] else ''
            ci_key = (CIK.lower(), Ticker.lower(), CompanyNameIssuer.lower())
            key_to_row[ci_key] = row
        
        # Process database data
        updated_rows = []
        
        for db_row in db_data:
            db_row = list(db_row)
            # Extract keys from the DB row
            CIK = db_row[18].strip() if db_row[18] else ''
            Ticker = db_row[0].strip() if db_row[0] else ''
            CompanyNameIssuer = db_row[2].strip() if db_row[2] else ''
            
            # Lowercased key for lookup
            ci_key = (CIK.lower(), Ticker.lower(), CompanyNameIssuer.lower())
            
            if ci_key in key_to_row:
                # Existing row in CSV
                csv_row = key_to_row[ci_key]
                # Update only source-of-truth columns
                for i in self.source_of_truth_columns:
                    if i < len(db_row):
                        csv_row[i] = db_row[i] if db_row[i] else ''
                updated_rows.append(csv_row)
                # Remove from mapping to track processed rows
                del key_to_row[ci_key]
            else:
                # New row from database
                new_row = [''] * 27
                for i in range(min(len(db_row), 27)):
                    new_row[i] = db_row[i] if db_row[i] else ''
                updated_rows.append(new_row)
        
        # Add any remaining CSV rows that weren't in the database
        updated_rows.extend(key_to_row.values())
        
        # Read headers from file
        with open(self.csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            try:
                headers = next(reader)
            except StopIteration:
                # Use default headers if file is empty
                headers = [
                    "Ticker", "Exchange", "Company_Name_Issuer", "Transfer_Agent", "Online_Purchase",
                    "DTC_Member_Number", "TA_URL", "Transfer_Agent_Pct", "IR_Emails", "IR_Phone_Number",
                    "IR_Company_Address", "IR_URL", "IR_Contact_Info", "Shares_Outstanding", "CUSIP",
                    "Company_Info_URL", "Company_Info", "Full_Progress_Pct", "CIK", "DRS",
                    "Percent_Shares_DRSd", "Submission_Received", "Timestamps_UTC", "Learn_More_About_DRS",
                    "Certificates_Offered", "S_And_P_500", "Incorporated_In"
                ]
        
        # Write updated data back to CSV
        with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(updated_rows)
            
        print(f"CSV updated successfully at {self.csv_file_path}")


class MultipleCSVHandler:
    def __init__(self, csv_dir_path, source_of_truth_columns):
        self.csv_dir_path = csv_dir_path
        self.source_of_truth_columns = source_of_truth_columns
        
        # Ensure directory exists
        os.makedirs(self.csv_dir_path, exist_ok=True)
        
        # Default headers
        self.headers = [
            "Ticker", "Exchange", "Company_Name_Issuer", "Transfer_Agent", "Online_Purchase",
            "DTC_Member_Number", "TA_URL", "Transfer_Agent_Pct", "IR_Emails", "IR_Phone_Number",
            "IR_Company_Address", "IR_URL", "IR_Contact_Info", "Shares_Outstanding", "CUSIP",
            "Company_Info_URL", "Company_Info", "Full_Progress_Pct", "CIK", "DRS",
            "Percent_Shares_DRSd", "Submission_Received", "Timestamps_UTC", "Learn_More_About_DRS",
            "Certificates_Offered", "S_And_P_500", "Incorporated_In"
        ]
        
        # Initialize CSV files if they don't exist
        self._initialize_csv_files()
    
    def _get_file_path_for_letter(self, letter):
        # Handle symbols and numbers - group them into "SPECIAL" file
        if not letter.isalpha():
            letter = "SPECIAL"
        else:
            letter = letter.upper()
        
        return os.path.join(self.csv_dir_path, f"{letter}.csv")
    
    def _initialize_csv_files(self):
        # Create alphabetical files (A-Z) and one for special characters
        for letter in list(string.ascii_uppercase) + ["SPECIAL"]:
            file_path = self._get_file_path_for_letter(letter)
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(self.headers)
    
    def read_csv_data(self):
        all_data = []
        
        # Read data from all CSV files
        for letter in list(string.ascii_uppercase) + ["SPECIAL"]:
            file_path = self._get_file_path_for_letter(letter)
            if os.path.exists(file_path):
                with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    data = list(reader)
                    if data and len(data) > 1:  # If there's data beyond headers
                        # Skip the header row
                        all_data.extend(data[1:])
        
        return all_data
    
    def update_csv(self, db_data):
        # Read existing CSV data to create a mapping
        existing_data = self.read_csv_data()
        
        # Create a mapping from lowercase (CIK, Ticker, CompanyNameIssuer) to row
        key_to_row = {}
        for row in existing_data:
            # Ensure row has at least 19 elements to access CIK
            row = row + [''] * (27 - len(row))
            CIK = row[18].strip() if row[18] else ''
            Ticker = row[0].strip() if row[0] else ''
            CompanyNameIssuer = row[2].strip() if row[2] else ''
            ci_key = (CIK.lower(), Ticker.lower(), CompanyNameIssuer.lower())
            key_to_row[ci_key] = row
        
        # Process database data
        letter_to_rows = {}
        
        # First, add all existing CSV rows to their respective letter files
        for row in existing_data:
            ticker = row[0].strip() if row[0] else ''
            first_letter = ticker[0].upper() if ticker else "SPECIAL"
            if not first_letter.isalpha():
                first_letter = "SPECIAL"
            
            if first_letter not in letter_to_rows:
                letter_to_rows[first_letter] = []
            letter_to_rows[first_letter].append(row)
        
        # Then process database data, updating existing rows and adding new ones
        for db_row in db_data:
            db_row = list(db_row)
            # Extract keys from the DB row
            CIK = db_row[18].strip() if db_row[18] else ''
            Ticker = db_row[0].strip() if db_row[0] else ''
            CompanyNameIssuer = db_row[2].strip() if db_row[2] else ''
            
            # Determine which letter file this row belongs to
            first_letter = Ticker[0].upper() if Ticker else "SPECIAL"
            if not first_letter.isalpha():
                first_letter = "SPECIAL"
            
            # Lowercased key for lookup
            ci_key = (CIK.lower(), Ticker.lower(), CompanyNameIssuer.lower())
            
            if ci_key in key_to_row:
                # Update existing row with source-of-truth columns
                csv_row = key_to_row[ci_key]
                for i in self.source_of_truth_columns:
                    if i < len(db_row):
                        csv_row[i] = db_row[i] if db_row[i] else ''
                
                # Find and update the row in letter_to_rows
                if first_letter in letter_to_rows:
                    for i, row in enumerate(letter_to_rows[first_letter]):
                        row_key = (
                            row[18].strip().lower() if row[18] else '',
                            row[0].strip().lower() if row[0] else '',
                            row[2].strip().lower() if row[2] else ''
                        )
                        if row_key == ci_key:
                            letter_to_rows[first_letter][i] = csv_row
                            break
            else:
                # New row from database
                new_row = [''] * 27
                for i in range(min(len(db_row), 27)):
                    new_row[i] = db_row[i] if db_row[i] else ''
                
                # Add to the appropriate letter file
                if first_letter not in letter_to_rows:
                    letter_to_rows[first_letter] = []
                letter_to_rows[first_letter].append(new_row)
        
        # Write updated data back to CSV files
        for letter, rows in letter_to_rows.items():
            file_path = self._get_file_path_for_letter(letter)
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.headers)
                writer.writerows(rows)
            print(f"CSV updated successfully at {file_path}")
            
        # Ensure all letter files exist, even if empty (with just headers)
        self._initialize_csv_files()
        
    def export_to_single_csv(self, output_file_path):
        """Export all data to a single CSV file for backward compatibility"""
        data = self.read_csv_data()
        
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.headers)
            writer.writerows(data)
            
        print(f"Exported all data to a single CSV file at {output_file_path}") 