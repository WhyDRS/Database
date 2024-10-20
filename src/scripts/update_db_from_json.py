import pandas as pd
import os
import json
import sqlite3

# Path to the JSON file
json_file_path = 'data/company_tickers_exchange.json'
db_file_path = 'data/Full_Database_Backend.db'

# Read the JSON file
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Extract fields and data
fields = data['fields']
records = data['data']

# Convert to DataFrame
df = pd.DataFrame(records, columns=fields)

# Replace NaN values with empty strings
df = df.fillna('')

# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Update the database with the JSON data
for index, row in df.iterrows():
    cursor.execute('''
        INSERT INTO full_database_backend (CIK, Ticker, Exchange, CompanyNameIssuer)
        VALUES (?, ?, ?, ?)
        ON CONFLICT (CIK, Ticker) DO UPDATE SET
            Exchange = excluded.Exchange,
            CompanyNameIssuer = excluded.CompanyNameIssuer
    ''', (row['cik'], row['ticker'], row['exchange'], row['name']))

# Replace NULL, blank, and single space values with empty strings
cursor.execute('''
    UPDATE full_database_backend
    SET
        Ticker = IFNULL(NULLIF(TRIM(Ticker), ''), ''),
        Exchange = IFNULL(NULLIF(TRIM(Exchange), ''), ''),
        CompanyNameIssuer = IFNULL(NULLIF(TRIM(CompanyNameIssuer), ''), ''),
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
        CIK = IFNULL(NULLIF(TRIM(CIK), ''), ''),
        DRS = IFNULL(NULLIF(TRIM(DRS), ''), ''),
        PercentSharesDRSd = IFNULL(NULLIF(TRIM(PercentSharesDRSd), ''), ''),
        SubmissionReceived = IFNULL(NULLIF(TRIM(SubmissionReceived), ''), ''),
        TimestampsUTC = IFNULL(NULLIF(TRIM(TimestampsUTC), ''), ''),
        LearnMoreAboutDRS = IFNULL(NULLIF(TRIM(LearnMoreAboutDRS), ''), ''),
        CertificatesOffered = IFNULL(NULLIF(TRIM(CertificatesOffered), ''), ''),
        SandP500 = IFNULL(NULLIF(TRIM(SandP500), ''), ''),
        IncorporatedIn = IFNULL(NULLIF(TRIM(IncorporatedIn), ''), '')
''')

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print(f"Database updated with data from {json_file_path}")
