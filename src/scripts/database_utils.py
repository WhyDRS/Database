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
        # Define column names
        columns = [f'col{i}' for i in range(27)]
        columns_sql = ',\n'.join([f'{col} TEXT' for col in columns])
        primary_keys = 'col18, col0, col2'  # CIK, Ticker, CompanyNameIssuer

        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS full_database_backend (
            {columns_sql},
            PRIMARY KEY ({primary_keys})
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
        for _, row in df_updates.iterrows():
            CIK = row['col18']  # 19th column
            Ticker = row['col0']  # 1st column
            CompanyNameIssuer = row['col2']  # 3rd column
            columns_to_update = [f'col{i}' for i in range(27) if i not in [0, 2, 18] and pd.notna(row[f'col{i}'])]
            set_clause = ', '.join([f"{col} = ?" for col in columns_to_update])
            values = [row[col] for col in columns_to_update]
            values.extend([CIK, Ticker, CompanyNameIssuer])

            if set_clause:
                sql = f"UPDATE full_database_backend SET {set_clause} WHERE col18 = ? AND col0 = ? AND col2 = ?"
                cursor.execute(sql, values)
                if cursor.rowcount == 0:
                    # Insert new record
                    placeholders = ', '.join(['?'] * 27)
                    insert_values = [row[f'col{i}'] if pd.notna(row[f'col{i}']) else '' for i in range(27)]
                    sql_insert = f"INSERT INTO full_database_backend VALUES ({placeholders})"
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
