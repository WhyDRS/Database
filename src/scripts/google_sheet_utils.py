import gspread
import pandas as pd

class GoogleSheetHandler:
    def __init__(self, sheet_id, creds_json):
        self.gc = gspread.service_account_from_dict(creds_json)
        self.sheet = self.gc.open_by_key(sheet_id)

    def read_sheet_to_dataframe(self, worksheet_name):
        worksheet = self.sheet.worksheet(worksheet_name)
        data = worksheet.get_all_values()
        headers = data[0]
        records = data[1:]
        df_sheet = pd.DataFrame(records, columns=headers)
        return df_sheet

    def update_google_sheet(self, worksheet_name, df_updates):
        if df_updates.empty:
            print("No updates to apply to the Google Sheet.")
            return

        worksheet = self.sheet.worksheet(worksheet_name)
        headers = worksheet.row_values(1)
        data = worksheet.get_all_values()
        records = data[1:]
        df_sheet_all = pd.DataFrame(records, columns=headers)
        df_sheet_all['Row_Number'] = range(2, len(df_sheet_all) + 2)
        df_sheet_all['CIK'] = df_sheet_all['CIK'].fillna('')
        df_sheet_all['Ticker'] = df_sheet_all['Ticker'].fillna('')
        key_to_row = df_sheet_all.set_index(['CIK', 'Ticker'])['Row_Number'].to_dict()

        updates = []
        new_rows = []
        for index, row in df_updates.iterrows():
            CIK = row['CIK']
            Ticker = row['Ticker']
            key = (CIK, Ticker)
            if key in key_to_row:
                row_number = key_to_row[key]
                for col in df_updates.columns:
                    if col not in ['CIK', 'Ticker'] and pd.notna(row[col]):
                        col_index = headers.index(col) + 1
                        cell = gspread.Cell(row_number, col_index, row[col])
                        updates.append(cell)
            else:
                new_row = [row.get(col, '') if pd.notna(row.get(col, '')) else '' for col in headers]
                new_rows.append(new_row)

        if updates:
            worksheet.update_cells(updates, value_input_option='USER_ENTERED')
            print(f"Updated {len(updates)} cells in Google Sheet.")

        if new_rows:
            worksheet.append_rows(new_rows, value_input_option='USER_ENTERED')
            print(f"Added {len(new_rows)} new rows to Google Sheet.")
