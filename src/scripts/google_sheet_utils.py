import gspread
import pandas as pd

class GoogleSheetHandler:
    def __init__(self, sheet_id, creds_json):
        self.gc = gspread.service_account_from_dict(creds_json)
        self.sheet = self.gc.open_by_key(sheet_id)

    def read_sheet_data(self, worksheet_name):
        worksheet = self.sheet.worksheet(worksheet_name)
        data = worksheet.get_all_values()
        data = [row[:27] for row in data[1:]]  # Skip header row
        return data

    def update_google_sheet(self, worksheet_name, db_data):
        worksheet = self.sheet.worksheet(worksheet_name)
        existing_data = worksheet.get_all_values()
        existing_data = [row[:27] for row in existing_data]
        headers = existing_data[0]
        records = existing_data[1:]
        key_to_row = {}
        for idx, row in enumerate(records):
            row = row + [''] * (27 - len(row))
            CIK, Ticker, CompanyNameIssuer = row[18], row[0], row[2]
            key = (CIK, Ticker, CompanyNameIssuer)
            key_to_row[key] = idx + 2  # Adjust for header row

        updates = []
        for db_row in db_data:
            CIK, Ticker, CompanyNameIssuer = db_row[18], db_row[0], db_row[2]
            key = (CIK, Ticker, CompanyNameIssuer)
            if key in key_to_row:
                row_number = key_to_row[key]
                sheet_row = worksheet.row_values(row_number)
                sheet_row = sheet_row + [''] * (27 - len(sheet_row))
                
                # Resolve conflict by selecting source with more filled cells
                sheet_filled = sum(1 for cell in sheet_row if cell)
                db_filled = sum(1 for cell in db_row if cell)
                if db_filled > sheet_filled:
                    updates.extend(
                        [gspread.Cell(row_number, col + 1, db_row[col]) for col in range(27) if sheet_row[col] != db_row[col]]
                    )
            else:
                new_row = [db_row[i] if db_row[i] else '' for i in range(27)]
                worksheet.append_row(new_row, value_input_option='USER_ENTERED')
                print(f"Added new row for key {key} to Google Sheet.")

        if updates:
            worksheet.update_cells(updates, value_input_option='USER_ENTERED')
            print(f"Updated {len(updates)} cells in Google Sheet.")
