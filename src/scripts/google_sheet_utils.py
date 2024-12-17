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
        worksheet_name_quoted = f"'{worksheet.title}'"

        existing_data = worksheet.get_all_values()
        if not existing_data:
            # If the sheet is empty or missing headers, just return (no updates can be done)
            return

        existing_data = [row[:27] for row in existing_data]
        headers = existing_data[0]
        records = existing_data[1:]

        # Create a mapping from (CIK, Ticker, CompanyNameIssuer) - case-insensitive - to row index (1-based)
        key_to_row = {}
        for idx, row in enumerate(records):
            row = row + [''] * (27 - len(row))
            CIK = (row[18] or '').lower()
            Ticker = (row[0] or '').lower()
            CompanyNameIssuer = (row[2] or '').lower()
            key = (CIK, Ticker, CompanyNameIssuer)
            key_to_row[key] = idx + 2  # row index after the header

        updates = []
        new_rows = []
        for db_row in db_data:
            db_row = list(db_row)
            CIK = (db_row[18] or '').lower()
            Ticker = (db_row[0] or '').lower()
            CompanyNameIssuer = (db_row[2] or '').lower()
            key = (CIK, Ticker, CompanyNameIssuer)

            if key in key_to_row:
                # Existing record in sheet
                row_number = key_to_row[key]
                sheet_row = records[row_number - 2]
                sheet_row = sheet_row + [''] * (27 - len(sheet_row))

                # Update only source-of-truth columns
                for i in self.source_of_truth_columns:
                    db_value = db_row[i] if i < len(db_row) else ''
                    sheet_value = sheet_row[i]
                    # If DB value is different (or sheet is blank), update
                    if db_value and db_value != sheet_value:
                        updates.append(gspread.Cell(row_number, i + 1, db_value))
            else:
                # New record not found in sheet; append only source-of-truth columns
                new_row = [''] * 27
                for i in self.source_of_truth_columns:
                    if i < len(db_row):
                        new_row[i] = db_row[i] if db_row[i] else ''
                new_rows.append(new_row)

        # Batch update source-of-truth columns if needed
        if updates:
            worksheet.update_cells(updates, value_input_option='USER_ENTERED')

        # Batch append new rows if any
        if new_rows:
            # Calculate the start row for new entries
            existing_record_count = len(records)
            start_row = existing_record_count + 2  # Because header is row 1, first record at row 2
            end_row = start_row + len(new_rows) - 1

            # We'll write these new rows into a contiguous range
            # Columns: A to AA for 27 columns
            update_range = f"{worksheet_name_quoted}!A{start_row}:AA{end_row}"
            worksheet.batch_update([{
                "range": update_range,
                "values": new_rows
            }], value_input_option='USER_ENTERED')
