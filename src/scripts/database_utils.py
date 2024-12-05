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
            # Ensure row has exactly 27 elements
            row = row + [''] * (27 - len(row))
            # Prepare the INSERT OR REPLACE statement
            cursor.execute('''
            INSERT OR REPLACE INTO full_database_backend (
                Ticker, Exchange, CompanyNameIssuer, TransferAgent, OnlinePurchase, DTCMemberNum, TAURL,
                TransferAgentPct, IREmails, IRPhoneNum, IRCompanyAddress, IRURL, IRContactInfo, SharesOutstanding,
                CUSIP, CompanyInfoURL, CompanyInfo, FullProgressPct, CIK, DRS, PercentSharesDRSd, SubmissionReceived,
                TimestampsUTC, LearnMoreAboutDRS, CertificatesOffered, SandP500, IncorporatedIn
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(row))

        conn.commit()
        conn.close()
        print("Database updated successfully.")

    def read_database_data(self):
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM full_database_backend')
        rows = cursor.fetchall()
        conn.close()
        return rows

    def export_database_to_json(self, json_file_path):
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM full_database_backend')
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        data_json = [dict(zip(column_names, row)) for row in rows]
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data_json, f, ensure_ascii=False, indent=4)
        conn.close()
        print(f"Exported database to {json_file_path}")
