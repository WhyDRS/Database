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

        # Only consider the first 27 columns
        headers = headers[:27]
        records = [row[:27] + ['']*(27 - len(row)) for row in records]  # Ensure each row has 27 elements

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

        # Only consider the first 27 columns
        headers_27 = headers[:27]
        df_sheet_all = pd.DataFrame(records, columns=headers)
        df_sheet_all = df_sheet_all.iloc[:, :27]  # Only first 27 columns
        df_sheet_all['Row_Number'] = range(2, len(df_sheet_all) + 2)

        # Map column names using the provided headers
        column_mapping = self.get_column_mapping(headers_27)
        df_sheet_all.rename(columns=column_mapping, inplace=True)

        # Handle primary keys
        df_sheet_all['CIK'] = df_sheet_all['CIK'].fillna('')
        df_sheet_all['Ticker'] = df_sheet_all['Ticker'].fillna('')
        df_sheet_all['CompanyNameIssuer'] = df_sheet_all['CompanyNameIssuer'].fillna('')

        key_to_row = df_sheet_all.set_index(['CIK', 'Ticker', 'CompanyNameIssuer'])['Row_Number'].to_dict()

        updates = []
        new_rows = []
        for index, row in df_updates.iterrows():
            CIK = row['CIK']
            Ticker = row['Ticker']
            CompanyNameIssuer = row['CompanyNameIssuer']
            key = (CIK, Ticker, CompanyNameIssuer)
            if key in key_to_row:
                row_number = key_to_row[key]
                for col in df_updates.columns:
                    if col not in ['CIK', 'Ticker', 'CompanyNameIssuer'] and pd.notna(row[col]):
                        # Find the correct column index in the sheet
                        sheet_col_name = [k for k, v in column_mapping.items() if v == col][0]
                        if sheet_col_name in headers:
                            col_index = headers.index(sheet_col_name) + 1  # 1-based indexing
                            cell = gspread.Cell(row_number, col_index, row[col])
                            updates.append(cell)
            else:
                # Append a new row
                new_row = [row.get(column_mapping.get(col, col), '') if pd.notna(row.get(col, '')) else '' for col in headers_27]
                new_rows.append(new_row)

        if updates:
            worksheet.update_cells(updates, value_input_option='USER_ENTERED')
            print(f"Updated {len(updates)} cells in Google Sheet.")

        if new_rows:
            worksheet.append_rows(new_rows, value_input_option='USER_ENTERED')
            print(f"Added {len(new_rows)} new rows to Google Sheet.")

    def get_column_mapping(self, sheet_headers):
        # Mapping between Google Sheet headers and database columns
        mapping = {
            'Ticker': 'Ticker',
            'Exchange': 'Exchange',
            'Company Name/Issuer': 'CompanyNameIssuer',
            'Transfer Agent': 'TransferAgent',
            'Online Purchase?': 'OnlinePurchase',
            'DTC Member #': 'DTCMemberNum',
            'TA URL': 'TAURL',
            'Transfer Agent %': 'TransferAgentPct',
            'IR Emails': 'IREmails',
            'IR Phone #': 'IRPhoneNum',
            'IR /Company Address': 'IRCompanyAddress',
            'IR URL': 'IRURL',
            'IR Contact Info': 'IRContactInfo',
            'Shares Outstanding': 'SharesOutstanding',
            'CUSIP': 'CUSIP',
            'Company Info URL': 'CompanyInfoURL',
            'Company Info': 'CompanyInfo',
            'Full Progress %': 'FullProgressPct',
            'CIK': 'CIK',
            'DRS': 'DRS',
            "% of Shares DRS'd": 'PercentSharesDRSd',
            'Submission Received': 'SubmissionReceived',
            'Timestamps (UTC)': 'TimestampsUTC',
            'Learn More about DRS': 'LearnMoreAboutDRS',
            'Certificates offered?': 'CertificatesOffered',
            'S&P 500?': 'SandP500',
            'Incorporated in:': 'IncorporatedIn'
        }

        # Reverse mapping to handle headers not in mapping
        sheet_to_db = {}
        for header in sheet_headers:
            if header in mapping:
                sheet_to_db[header] = mapping[header]
            else:
                # Normalize and attempt to match
                normalized_header = header.strip().lower().replace(' ', '').replace('_', '').replace('?', '').replace('#', '').replace('/', '')
                for sheet_header, db_column in mapping.items():
                    normalized_sheet_header = sheet_header.strip().lower().replace(' ', '').replace('_', '').replace('?', '').replace('#', '').replace('/', '')
                    if normalized_header == normalized_sheet_header:
                        sheet_to_db[header] = db_column
                        break
                else:
                    # If no match found, map header to itself
                    sheet_to_db[header] = header

        return sheet_to_db
