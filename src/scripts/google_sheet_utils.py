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
        headers = data[0][:27]  # First 27 headers
        records = [row[:27] for row in data[1:]]  # First 27 columns of data
        df_sheet = pd.DataFrame(records, columns=headers)
        return df_sheet

    def update_google_sheet(self, worksheet_name, df_updates):
        if df_updates.empty:
            print("No updates to apply to the Google Sheet.")
            return

        worksheet = self.sheet.worksheet(worksheet_name)
        data = worksheet.get_all_values()
        # Use indexes since headers might differ
        records = data[1:]  # Exclude header
        total_rows = len(records)
        total_cols = len(data[0])

        # Build key to row mapping
        key_to_row = {}
        for idx, row in enumerate(records):
            # Ensure row has at least 27 columns
            row = row + [''] * (27 - len(row))
            CIK = row[18]  # 19th column
            Ticker = row[0]  # 1st column
            CompanyNameIssuer = row[2]  # 3rd column
            key = (CIK, Ticker, CompanyNameIssuer)
            key_to_row[key] = idx + 2  # Row numbers start from 2

        updates = []
        new_rows = []
        for index, row in df_updates.iterrows():
            CIK = row.iloc[18]  # 19th column
            Ticker = row.iloc[0]  # 1st column
            CompanyNameIssuer = row.iloc[2]  # 3rd column
            key = (CIK, Ticker, CompanyNameIssuer)
            if key in key_to_row:
                row_number = key_to_row[key]
                for col_idx in range(27):
                    if pd.notna(row.iloc[col_idx]):
                        cell = gspread.Cell(row_number, col_idx + 1, row.iloc[col_idx])
                        updates.append(cell)
            else:
                # Append new row
                new_row = [row.iloc[i] if pd.notna(row.iloc[i]) else '' for i in range(27)]
                new_rows.append(new_row)

        if updates:
            worksheet.update_cells(updates, value_input_option='USER_ENTERED')
            print(f"Updated {len(updates)} cells in Google Sheet.")

        if new_rows:
            worksheet.append_rows(new_rows, value_input_option='USER_ENTERED')
            print(f"Added {len(new_rows)} new rows to Google Sheet.")
