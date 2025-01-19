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
            cursor.execute('''
            INSERT OR REPLACE INTO full_database_backend (
                Ticker, Exchange, Company_Name_Issuer, Transfer_Agent, Online_Purchase, DTC_Member_Number, TA_URL,
                Transfer_Agent_Pct, IR_Emails, IR_Phone_Number, IR_Company_Address, IR_URL, IR_Contact_Info, Shares_Outstanding,
                CUSIP, Company_Info_URL, Company_Info, Full_Progress_Pct, CIK, DRS, Percent_Shares_DRSd, Submission_Received,
                Timestamps_UTC, Learn_More_About_DRS, Certificates_Offered, S_And_P_500, Incorporated_In
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
        column_names = [description[0].replace('_', ' ') for description in cursor.description]
        data_json = [dict(zip(column_names, row)) for row in rows]
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data_json, f, ensure_ascii=False, indent=4)
        conn.close()
        print(f"Exported database to {json_file_path}")
