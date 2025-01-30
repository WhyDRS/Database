import gspread  # Import gspread to interact with Google Sheets
import sqlite3  # Import sqlite3 to interact with SQLite databases
import os       # Import os module to interact with the operating system
import json     # Import json module for parsing and writing JSON data

# Load credentials from the environment variable
creds_json = json.loads(os.environ['GOOGLE_API_KEYS'])  # Parse JSON credentials from an environment variable

# Authenticate with the Google Sheets API
gc = gspread.service_account_from_dict(creds_json)  # Use credentials to authenticate and create a Google Sheets client

# Open the Google Sheet using the provided SHEET_ID
sheet = gc.open_by_key(os.environ['SHEET_ID'])  # Open the spreadsheet using the SHEET_ID from environment variables
worksheet = sheet.worksheet("Main_Database")  # Access the specific worksheet

# Get all values from columns A to AA (adjust the range if the sheet grows)
# Fetch all rows starting from the second row to the end of the worksheet and fill empty cells with a space
data = [row + [' ']*(27 - len(row)) for row in worksheet.get('A2:AA' + str(worksheet.row_count))]

# Connect to a SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('data/Main_Database.db')  # Establish a connection to a SQLite database
conn.row_factory = sqlite3.Row  # Configure the connection to use row factory, allowing for dictionary-like column access
cursor = conn.cursor()  # Create a cursor object to execute SQL commands

# Create a table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS Main_Database (
    Ticker TEXT PRIMARY KEY,
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
    IncorporatedIn TEXT
)
''')  # SQL command to create a new table if it doesn't already exist, with schema defined

# Insert or update values into the database
for row in data:
    # Log the number of elements in the current row
    print(f"Processing row with {len(row)} elements: {row}")

    # Check if the row has the correct number of elements (adjust 27 to match the expected number of columns)
    if len(row) == 27:
        cursor.execute('''
        INSERT OR REPLACE INTO Main_Database (
            Ticker, Exchange, CompanyNameIssuer, TransferAgent, OnlinePurchase, DTCMemberNum, TAURL,
            TransferAgentPct, IREmails, IRPhoneNum, IRCompanyAddress, IRURL, IRContactInfo, SharesOutstanding,
            CUSIP, CompanyInfoURL, CompanyInfo, FullProgressPct, CIK, DRS, PercentSharesDRSd, SubmissionReceived,
            TimestampsUTC, LearnMoreAboutDRS, CertificatesOffered, SandP500, IncorporatedIn
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(row))  # Execute an SQL command to insert or replace records in the database
    else:
        print(f"Skipping row due to incorrect number of elements: {row}")
        print(f"Row length: {len(row)}")  # Output the length of the row for debugging purposes

# Commit the changes to the SQL database
conn.commit()  # Commit all changes made during the transaction

# Now query all data from the database for JSON conversion
cursor.execute('SELECT * FROM Main_Database')  # Execute an SQL query to select all records from the table
rows = cursor.fetchall()  # Fetch all the rows from the query

# Convert the rows to dictionaries
data_json = [dict(ix) for ix in rows]  # Convert each row into a dictionary

# Write the data to a JSON file
with open('data/Main_Database.json', 'w', encoding='utf-8') as f:
    json.dump(data_json, f, ensure_ascii=False, indent=4)  # Write JSON data to a file with UTF-8 encoding and formatted

# Close the database connection
cursor.close()  # Close the cursor to free resources
conn.close()  # Close the connection to the database
