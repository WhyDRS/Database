import gspread
import pandas as pd

class GoogleSheetHandler:
    def __init__(self, sheet_id, creds_json):
        self.gc = gspread.service_account_from_dict(creds_json)
        self.sheet = self.gc.open_by_key(sheet_id)

    def read_sheet_data(self, worksheet_name):
        worksheet = self.sheet.worksheet(worksheet_name)
        # Read all data from the worksheet
        data = worksheet.get_all_values()
        # Only process the first 27 columns, skip the header row
        data = [row[:27] for row in data[1:]]  
        return data

    def update_google_sheet(self, worksheet_name, db_data):
        worksheet = self.sheet.worksheet(worksheet_name)
        # Get existing data in one call
        existing_data = worksheet.get_all_values()
        existing_data = [row[:27] for row in existing_data]  # Only first 27 columns
        headers = existing_data[0]
        records = existing_data[1:]

        # Create a mapping from (CIK, Ticker, CompanyNameIssuer) to row index (1-based in the sheet)
        key_to_row = {}
        for idx, row in enumerate(records):
            row = row + [''] * (27 - len(row))
            CIK = row[18]
            Ticker = row[0]
            CompanyNameIssuer = row[2]
            key = (CIK, Ticker, CompanyNameIssuer)
            key_to_row[key] = idx + 2  # Adjust for header row

        updates = []
        for row in db_data:
            CIK = row[18]
            Ticker = row[0]
            CompanyNameIssuer = row[2]
            key = (CIK, Ticker, CompanyNameIssuer)

            if key in key_to_row:
                # We already have this record in the sheet
                row_number = key_to_row[key]
                # Instead of calling row_values, use our cached `records` data
                sheet_row = records[row_number - 2]  # Adjusting since records start after headers
                sheet_row = sheet_row + [''] * (27 - len(sheet_row))

                # Identify missing cells and prepare updates
                for i in range(27):
                    if not sheet_row[i] and row[i]:
                        cell = gspread.Cell(row_number, i + 1, row[i])
                        updates.append(cell)
            else:
                # Append new row if key not found
                new_row = [row[i] if row[i] else '' for i in range(27)]
                worksheet.append_row(new_row, value_input_option='USER_ENTERED')
                print(f"Added new row for key {key} to Google Sheet.")

        if updates:
            # Batch update all cells at once
            worksheet.update_cells(updates, value_input_option='USER_ENTERED')
            print(f"Updated {len(updates)} cells in Google Sheet.")
