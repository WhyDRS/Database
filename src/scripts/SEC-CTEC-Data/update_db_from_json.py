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
    CompanyNameIssuer TEXT,
    TransferAgent TEXT,
    OnlinePurchase TEXT,
    DTCMemberNum TEXT,
    TAURL TEXT,
    TransferAgentPct TEXT,
    IREmails TEXT,
    IRPhoneNum TEXT,
    IRCompanyAddress TEXT,
    IRURL TEXT,
    IRContactInfo TEXT,
    SharesOutstanding TEXT,
    CUSIP TEXT,
    CompanyInfoURL TEXT,
    CompanyInfo TEXT,
    FullProgressPct TEXT,
    CIK TEXT,
    DRS TEXT,
    PercentSharesDRSd TEXT,
    SubmissionReceived TEXT,
    TimestampsUTC TEXT,
    LearnMoreAboutDRS TEXT,
    CertificatesOffered TEXT,
    SandP500 TEXT,
    IncorporatedIn TEXT,
    PRIMARY KEY (CIK, Ticker, CompanyNameIssuer)
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
        SET CIK = ?, Ticker = ?, Exchange = ?, CompanyNameIssuer = ?
        WHERE CIK = ?
          AND Ticker = ?
          AND LOWER(CompanyNameIssuer) = LOWER(?)
    ''', (
        cik_value, ticker_value, exchange_value, company_name_issuer_value,
        cik_value, ticker_value, company_name_issuer_value
    ))

    # If no rows were updated, INSERT a new one
    if cursor.rowcount == 0:
        cursor.execute('''
            INSERT INTO full_database_backend (CIK, Ticker, Exchange, CompanyNameIssuer)
            VALUES (?, ?, ?, ?)
        ''', (cik_value, ticker_value, exchange_value, company_name_issuer_value))

# Clean up whitespace and NULL-like values in non-key columns only
cursor.execute('''
UPDATE full_database_backend
SET
    Exchange = IFNULL(NULLIF(TRIM(Exchange), ''), ''),
    TransferAgent = IFNULL(NULLIF(TRIM(TransferAgent), ''), ''),
    OnlinePurchase = IFNULL(NULLIF(TRIM(OnlinePurchase), ''), ''),
    DTCMemberNum = IFNULL(NULLIF(TRIM(DTCMemberNum), ''), ''),
    TAURL = IFNULL(NULLIF(TRIM(TAURL), ''), ''),
    TransferAgentPct = IFNULL(NULLIF(TRIM(TransferAgentPct), ''), ''),
    IREmails = IFNULL(NULLIF(TRIM(IREmails), ''), ''),
    IRPhoneNum = IFNULL(NULLIF(TRIM(IRPhoneNum), ''), ''),
    IRCompanyAddress = IFNULL(NULLIF(TRIM(IRCompanyAddress), ''), ''),
    IRURL = IFNULL(NULLIF(TRIM(IRURL), ''), ''),
    IRContactInfo = IFNULL(NULLIF(TRIM(IRContactInfo), ''), ''),
    SharesOutstanding = IFNULL(NULLIF(TRIM(SharesOutstanding), ''), ''),
    CUSIP = IFNULL(NULLIF(TRIM(CUSIP), ''), ''),
    CompanyInfoURL = IFNULL(NULLIF(TRIM(CompanyInfoURL), ''), ''),
    CompanyInfo = IFNULL(NULLIF(TRIM(CompanyInfo), ''), ''),
    FullProgressPct = IFNULL(NULLIF(TRIM(FullProgressPct), ''), ''),
    DRS = IFNULL(NULLIF(TRIM(DRS), ''), ''),
    PercentSharesDRSd = IFNULL(NULLIF(TRIM(PercentSharesDRSd), ''), ''),
    SubmissionReceived = IFNULL(NULLIF(TRIM(SubmissionReceived), ''), ''),
    TimestampsUTC = IFNULL(NULLIF(TRIM(TimestampsUTC), ''), ''),
    LearnMoreAboutDRS = IFNULL(NULLIF(TRIM(LearnMoreAboutDRS), ''), ''),
    CertificatesOffered = IFNULL(NULLIF(TRIM(CertificatesOffered), ''), ''),
    SandP500 = IFNULL(NULLIF(TRIM(SandP500), ''), ''),
    IncorporatedIn = IFNULL(NULLIF(TRIM(IncorporatedIn), ''), '')
''')

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()

print(f"Database updated from {JSON_FILE_PATH} successfully.")
