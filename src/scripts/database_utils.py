import sqlite3
import pandas as pd
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

    def read_database_to_dataframe(self):
        conn = sqlite3.connect(self.db_file_path)
        query = "SELECT * FROM full_database_backend"
        df_db = pd.read_sql_query(query, conn)
        conn.close()
        return df_db

    def update_database(self, df_updates):
        if df_updates.empty:
            print("No updates to apply to the database.")
            return

        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()
        for index, row in df_updates.iterrows():
            CIK = row['CIK']
            Ticker = row['Ticker']
            CompanyNameIssuer = row['CompanyNameIssuer']
            columns_to_update = [col for col in df_updates.columns if col not in ['CIK', 'Ticker', 'CompanyNameIssuer'] and pd.notna(row[col])]
            set_clause = ', '.join([f"{col} = ?" for col in columns_to_update])
            values = [row[col] for col in columns_to_update]
            values.extend([CIK, Ticker, CompanyNameIssuer])

            if set_clause:
                sql = f"UPDATE full_database_backend SET {set_clause} WHERE CIK = ? AND Ticker = ? AND CompanyNameIssuer = ?"
                cursor.execute(sql, values)
                if cursor.rowcount == 0:
                    # Insert new record
                    columns = ['CIK', 'Ticker', 'CompanyNameIssuer'] + columns_to_update
                    placeholders = ', '.join(['?'] * len(columns))
                    insert_values = [row[col] for col in columns]
                    sql_insert = f"INSERT INTO full_database_backend ({', '.join(columns)}) VALUES ({placeholders})"
                    cursor.execute(sql_insert, insert_values)
            else:
                print(f"No updates for record with CIK={CIK}, Ticker={Ticker}, CompanyNameIssuer={CompanyNameIssuer}")

        conn.commit()
        conn.close()
        print("Database updated successfully.")

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
