import gspread
import pandas as pd

class GoogleSheetHandler:
    def __init__(self, sheet_id, creds_json):
        self.gc = gspread.service_account_from_dict(creds_json)
        self.sheet = self.gc.open_by_key(sheet_id)

    def read_sheet_to_dataframe(self, worksheet_name):
        worksheet = self.sheet.worksheet(worksheet_name)
        # Read only the first 27 columns
        data = worksheet.get_all_values()
        records = [row[:27] for row in data[1:]]  # First 27 columns of data
        df_sheet = pd.DataFrame(records)
        return df_sheet

    def update_google_sheet(self, worksheet_name, df_updates):
        if df_updates.empty:
            print("No updates to apply to the Google Sheet.")
            return

        worksheet = self.sheet.worksheet(worksheet_name)
        data = worksheet.get_all_values()
        total_rows = len(data)
        total_cols = len(data[0])

        # Build key to row mapping
        key_to_row = {}
        for idx, row in enumerate(data[1:], start=2):  # Start at row 2 (excluding headers)
            row = row + [''] * (27 - len(row))
            CIK = row[18]
            Ticker = row[0]
            CompanyNameIssuer = row[2]
            key = (CIK, Ticker, CompanyNameIssuer)
            key_to_row[key] = idx

        updates = []
        for _, row in df_updates.iterrows():
            CIK = row['col18']
            Ticker = row['col0']
            CompanyNameIssuer = row['col2']
            key = (CIK, Ticker, CompanyNameIssuer)
            if key in key_to_row:
                row_number = key_to_row[key]
                for i in range(27):
                    if i in [0, 2, 18]:
                        continue
                    if pd.notna(row[f'col{i}']):
                        cell = gspread.Cell(row_number, i + 1, row[f'col{i}'])
                        updates.append(cell)
            else:
                print(f"Key {key} not found in Google Sheet; cannot update.")

        if updates:
            worksheet.update_cells(updates, value_input_option='USER_ENTERED')
            print(f"Updated {len(updates)} cells in Google Sheet.")
