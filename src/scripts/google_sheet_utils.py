import gspread

class GoogleSheetHandler:
    def __init__(self, sheet_id, creds_json):
        self.gc = gspread.service_account_from_dict(creds_json)
        self.sheet = self.gc.open_by_key(sheet_id)

    def read_sheet_data(self, worksheet_name):
        worksheet = self.sheet.worksheet(worksheet_name)
        # Read all data from the worksheet
        data = worksheet.get_all_values()
        # Only process the first 27 columns
        data = [row[:27] for row in data[1:]]  # Skip header row
        return data

    def update_google_sheet(self, worksheet_name, db_data):
        worksheet = self.sheet.worksheet(worksheet_name)
        # Get existing data to build key mapping
        existing_data = worksheet.get_all_values()
        existing_data = [row[:27] for row in existing_data]  # Only first 27 columns
        headers = existing_data[0]
        records = existing_data[1:]
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
            # Ensure row has exactly 27 elements
            row = list(row)
            row = row + [''] * (27 - len(row))
            CIK = row[18]
            Ticker = row[0]
            CompanyNameIssuer = row[2]
            key = (CIK, Ticker, CompanyNameIssuer)
            if key in key_to_row:
                row_number = key_to_row[key]
                # Get the existing row from Google Sheet
                sheet_row = worksheet.row_values(row_number)
                sheet_row = sheet_row + [''] * (27 - len(sheet_row))

                # Compare the number of non-empty cells
                db_non_empty = sum(1 for cell in row if str(cell).strip())
                sheet_non_empty = sum(1 for cell in sheet_row if cell.strip())

                if db_non_empty > sheet_non_empty:
                    # Update the entire row in Google Sheet with data from database
                    cell_list = worksheet.range(row_number, 1, row_number, 27)
                    for i, cell in enumerate(cell_list):
                        cell.value = row[i] if row[i] else ''
                    updates.extend(cell_list)
                    print(f"Updated row {row_number} in Google Sheet for key {key} with data from database.")
                else:
                    # Keep the existing Google Sheet row
                    print(f"Kept existing Google Sheet row for key {key}.")
            else:
                # Append new row
                new_row = [row[i] if row[i] else '' for i in range(27)]
                worksheet.append_row(new_row, value_input_option='USER_ENTERED')
                print(f"Added new row for key {key} to Google Sheet.")

        if updates:
            worksheet.update_cells(updates, value_input_option='USER_ENTERED')
            print(f"Updated {len(updates)} cells in Google Sheet.")
