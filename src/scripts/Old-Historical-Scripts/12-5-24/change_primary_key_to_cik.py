import sqlite3

db_file_path = 'data/test.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Create a new table with the correct schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS test_new (
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
    PRIMARY KEY (CIK, Ticker)  -- CIK as primary key, Ticker as secondary key
)
''')

# Migrate data from the old table to the new table
cursor.execute('''
INSERT INTO test_new
SELECT * FROM test
''')

# Drop the old table
cursor.execute('DROP TABLE test')

# Rename the new table to the old table name
cursor.execute('ALTER TABLE test_new RENAME TO test')

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Database schema updated successfully.")
