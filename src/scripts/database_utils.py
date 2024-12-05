import sqlite3
import json

class DatabaseHandler:
    def __init__(self, db_file_path):
        self.db_file_path = db_file_path
        self.ensure_database_schema()

    def ensure_database_schema(self):
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()
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
        conn.commit()
        conn.close()

    def update_database(self, data):
        if not data:
            print("No data to update in the database.")
            return

        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()

        for row in data:
            row = row + [''] * (27 - len(row))
            cursor.execute('SELECT * FROM full_database_backend WHERE CIK=? AND Ticker=? AND CompanyNameIssuer=?',
                           (row[18], row[0], row[2]))
            db_row = cursor.fetchone()
            if db_row:
                db_filled = sum(1 for cell in db_row if cell)
                sheet_filled = sum(1 for cell in row if cell)
                if sheet_filled > db_filled:
                    cursor.execute('''
                    REPLACE INTO full_database_backend VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', tuple(row))
            else:
                cursor.execute('''
                INSERT INTO full_database_backend VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', tuple(row))

        conn.commit()
        conn.close()
        print("Database updated successfully.")
