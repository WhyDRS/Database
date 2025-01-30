import sqlite3

<<<<<<<< HEAD:src/scripts/Update_Issuers_TA_DB/change_primary_key_to_cik.py
db_file_path = 'data/Issuers_TA/Issuers_TA.db'
========
db_file_path = 'data/Main_Database.db'
>>>>>>>> 19bfdc4836497caaef74ddce4c6b3e76a486403d:src/scripts/Old-Historical-Scripts/12-5-24/change_primary_key_to_cik.py

# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Create a new table with the correct schema
cursor.execute('''
<<<<<<<< HEAD:src/scripts/Update_Issuers_TA_DB/change_primary_key_to_cik.py
CREATE TABLE IF NOT EXISTS Issuers_TA_new (
========
CREATE TABLE IF NOT EXISTS Main_Database_new (
>>>>>>>> 19bfdc4836497caaef74ddce4c6b3e76a486403d:src/scripts/Old-Historical-Scripts/12-5-24/change_primary_key_to_cik.py
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
<<<<<<<< HEAD:src/scripts/Update_Issuers_TA_DB/change_primary_key_to_cik.py
INSERT INTO Issuers_TA_new
SELECT * FROM Issuers_TA
''')

# Drop the old table
cursor.execute('DROP TABLE Issuers_TA')

# Rename the new table to the old table name
cursor.execute('ALTER TABLE Issuers_TA_new RENAME TO Issers_TA')
========
INSERT INTO Main_Database_new
SELECT * FROM Main_Database
''')

# Drop the old table
cursor.execute('DROP TABLE Main_Database')

# Rename the new table to the old table name
cursor.execute('ALTER TABLE Main_Database_new RENAME TO Main_Database')
>>>>>>>> 19bfdc4836497caaef74ddce4c6b3e76a486403d:src/scripts/Old-Historical-Scripts/12-5-24/change_primary_key_to_cik.py

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Database schema updated successfully.")
