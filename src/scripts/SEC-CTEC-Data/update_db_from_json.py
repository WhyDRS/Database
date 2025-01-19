import pandas as pd
import json
import sqlite3

# File paths
JSON_FILE_PATH = 'data/SEC-CTEC-Data/company_tickers_exchange.json'
DB_FILE_PATH = 'data/Issuers/Full_Database_Backend.db'

# Read JSON data
with open(JSON_FILE_PATH, 'r') as json_file:
    sec_data = json.load(json_file)

fields = sec_data['fields']
records = sec_data['data']

# Convert JSON records to a DataFrame
df = pd.DataFrame(records, columns=fields)

# Replace NaN with empty strings
df = df.fillna('')

# Deduplicate based on primary key columns from SEC data
df.drop_duplicates(subset=['cik', 'ticker', 'name'], inplace=True)

# Connect to the SQLite database
conn = sqlite3.connect(DB_FILE_PATH)
cursor = conn.cursor()

# Create table with the updated schema if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS full_database_backend (
    Ticker TEXT,
    Exchange TEXT,
    Company_Name_Issuer TEXT,
    Transfer_Agent TEXT,
    Online_Purchase TEXT,
    DTC_Member_Number TEXT,
    TA_URL TEXT,
    Transfer_Agent_Pct TEXT,
    IR_Emails TEXT,
    IR_Phone_Number TEXT,
    IR_Company_Address TEXT,
    IR_URL TEXT,
    IR_Contact_Info TEXT,
    Shares_Outstanding TEXT,
    CUSIP TEXT,
    Company_Info_URL TEXT,
    Company_Info TEXT,
    Full_Progress_Pct TEXT,
    CIK TEXT,
    DRS TEXT,
    Percent_Shares_DRSd TEXT,
    Submission_Received TEXT,
    Timestamps_UTC TEXT,
    Learn_More_About_DRS TEXT,
    Certificates_Offered TEXT,
    S_And_P_500 TEXT,
    Incorporated_In TEXT,
    PRIMARY KEY (CIK, Ticker, Company_Name_Issuer)
)
''')

# Update existing rows or insert new rows from SEC data
# Use case-insensitive matching for CompanyNameIssuer to detect conflicts.
for _, row in df.iterrows():
    cik_value = row['cik']
    ticker_value = row['ticker']
    exchange_value = row['exchange']
    company_name_issuer_value = row['name']

    # Attempt to UPDATE existing row, ignoring case differences in CompanyNameIssuer
    cursor.execute('''
        UPDATE full_database_backend
        SET CIK = ?, Ticker = ?, Exchange = ?, Company_Name_Issuer = ?
        WHERE CIK = ?
          AND Ticker = ?
          AND LOWER(Company_Name_Issuer) = LOWER(?)
    ''', (
        cik_value, ticker_value, exchange_value, company_name_issuer_value,
        cik_value, ticker_value, company_name_issuer_value
    ))

    # If no rows were updated, INSERT a new one
    if cursor.rowcount == 0:
        cursor.execute('''
            INSERT INTO full_database_backend (CIK, Ticker, Exchange, Company_Name_Issuer)
            VALUES (?, ?, ?, ?)
        ''', (cik_value, ticker_value, exchange_value, company_name_issuer_value))

# Clean up whitespace and NULL-like values in non-key columns only
cursor.execute('''
UPDATE full_database_backend
SET
    Exchange = IFNULL(NULLIF(TRIM(Exchange), ''), ''),
    Transfer_Agent = IFNULL(NULLIF(TRIM(Transfer_Agent), ''), ''),
    Online_Purchase = IFNULL(NULLIF(TRIM(Online_Purchase), ''), ''),
    DTC_Member_Number = IFNULL(NULLIF(TRIM(DTC_Member_Number), ''), ''),
    TA_URL = IFNULL(NULLIF(TRIM(TA_URL), ''), ''),
    Transfer_Agent_Pct = IFNULL(NULLIF(TRIM(Transfer_Agent_Pct), ''), ''),
    IREmails = IFNULL(NULLIF(TRIM(IREmails), ''), ''),
    IRPhoneNum = IFNULL(NULLIF(TRIM(IRPhoneNum), ''), ''),
    IRCompanyAddress = IFNULL(NULLIF(TRIM(IRCompanyAddress), ''), ''),
    IRURL = IFNULL(NULLIF(TRIM(IRURL), ''), ''),
    IRContactInfo = IFNULL(NULLIF(TRIM(IRContactInfo), ''), ''),
    SharesOutstanding = IFNULL(NULLIF(TRIM(SharesOutstanding), ''), ''),
    CUSIP = IFNULL(NULLIF(TRIM(CUSIP), ''), ''),
    Company_Info_URL = IFNULL(NULLIF(TRIM(Company_Info_URL), ''), ''),
    Company_Info = IFNULL(NULLIF(TRIM(Company_Info), ''), ''),
    Full_Progress_Pct = IFNULL(NULLIF(TRIM(Full_Progress_Pct), ''), ''),
    DRS = IFNULL(NULLIF(TRIM(DRS), ''), ''),
    Percent_Shares_DRSd = IFNULL(NULLIF(TRIM(Percent_Shares_DRSd), ''), ''),
    Submission_Received = IFNULL(NULLIF(TRIM(Submission_Received), ''), ''),
    Timestamps_UTC = IFNULL(NULLIF(TRIM(Timestamps_UTC), ''), ''),
    Learn_More_About_DRS = IFNULL(NULLIF(TRIM(Learn_More_About_DRS), ''), ''),
    Certificates_Offered = IFNULL(NULLIF(TRIM(Certificates_Offered), ''), ''),
    S_And_P_500 = IFNULL(NULLIF(TRIM(S_And_P_500), ''), ''),
    Incorporated_In = IFNULL(NULLIF(TRIM(Incorporated_In), ''), '')
''')

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()

print(f"Database updated from {JSON_FILE_PATH} successfully.")
