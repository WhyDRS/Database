import gspread

class GoogleSheetHandler:
    def __init__(self, sheet_id, creds_json, source_of_truth_columns):
        self.gc = gspread.service_account_from_dict(creds_json)
        self.sheet = self.gc.open_by_key(sheet_id)
        self.source_of_truth_columns = source_of_truth_columns

    def read_sheet_data(self, worksheet_name):
        worksheet = self.sheet.worksheet(worksheet_name)
        data = worksheet.get_all_values()
        if not data:
            return []
        # Only process the first 27 columns, skip the header row
        data = [row[:27] for row in data[1:]]  
        return data

    def update_google_sheet(self, worksheet_name, db_data):
        worksheet = self.sheet.worksheet(worksheet_name)
        existing_data = worksheet.get_all_values()
        if not existing_data:
            # If the sheet is empty or missing headers, we assume no header:
            return

        existing_data = [row[:27] for row in existing_data]
        headers = existing_data[0]
        records = existing_data[1:]

        # Create a mapping from lowercase (CIK, Ticker, CompanyNameIssuer) to a tuple of:
        # (row_index, original_row_values)
        key_to_row = {}
        for idx, row in enumerate(records):
            row = row + [''] * (27 - len(row))
            CIK = row[18].strip()
            Ticker = row[0].strip()
            CompanyNameIssuer = row[2].strip()

            # Case-insensitive key
            ci_key = (CIK.lower(), Ticker.lower(), CompanyNameIssuer.lower())
            key_to_row[ci_key] = (idx + 2, row)

        updates = []
        for db_row in db_data:
            db_row = list(db_row)
            # Extract keys from the DB row (source of truth)
            CIK = (db_row[18].strip() if db_row[18] else '')
            Ticker = (db_row[0].strip() if db_row[0] else '')
            CompanyNameIssuer = (db_row[2].strip() if db_row[2] else '')

            # Lowercased key for lookup
            ci_key = (CIK.lower(), Ticker.lower(), CompanyNameIssuer.lower())

            if ci_key in key_to_row:
                # Existing row in sheet
                row_number, sheet_row = key_to_row[ci_key]
                # Update only source-of-truth columns
                for i in self.source_of_truth_columns:
                    db_value = db_row[i] if i < len(db_row) else ''
                    sheet_value = sheet_row[i]
                    if db_value and db_value != sheet_value:
                        updates.append(gspread.Cell(row_number, i + 1, db_value))
            else:
                # Add a new row to the sheet with only the source-of-truth columns
                new_row = [''] * 27
                for i in self.source_of_truth_columns:
                    if i < len(db_row):
                        new_row[i] = db_row[i] if db_row[i] else ''
                worksheet.append_row(new_row, value_input_option='USER_ENTERED')

        # Batch update all source-of-truth columns if needed
        if updates:
            worksheet.update_cells(updates, value_input_option='USER_ENTERED')
