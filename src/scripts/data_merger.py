import pandas as pd

class DataMerger:
    def merge_dataframes(self, df_sheet, df_db):
        # We only consider the first 27 columns
        df_sheet = df_sheet.iloc[:, :27]
        df_db = df_db.iloc[:, :27]

        # Replace empty strings with NaN for comparison
        df_sheet.replace('', pd.NA, inplace=True)
        df_db.replace('', pd.NA, inplace=True)

        # Align the column names of df_db to match df_sheet
        df_db.columns = df_sheet.columns

        # Define key columns
        key_columns = [df_sheet.columns[18], df_sheet.columns[0], df_sheet.columns[2]]  # CIK, Ticker, CompanyNameIssuer

        # Merge on composite key (CIK, Ticker, CompanyNameIssuer)
        df_merged = pd.merge(
            df_sheet,
            df_db,
            on=key_columns,
            how='outer',
            suffixes=('_sheet', '_db'),
            indicator=True
        )

        df_db_updates = pd.DataFrame()
        df_sheet_updates = pd.DataFrame()

        for i in range(27):
            if i in [0, 2, 18]:  # Skip keys
                continue
            col_name = df_sheet.columns[i]
            col_sheet = col_name + '_sheet'
            col_db = col_name + '_db'

            # Check if the columns exist in df_merged
            if col_sheet not in df_merged.columns or col_db not in df_merged.columns:
                continue

            # Update database where DB has NaN and sheet has data
            condition_db_update = df_merged[col_db].isna() & df_merged[col_sheet].notna()
            if condition_db_update.any():
                update_rows = df_merged.loc[condition_db_update, key_columns + [col_sheet]].copy()
                update_rows.rename(columns={col_sheet: col_name}, inplace=True)
                df_db_updates = pd.concat([df_db_updates, update_rows], ignore_index=True)

            # Update sheet where sheet has NaN and DB has data
            condition_sheet_update = df_merged[col_sheet].isna() & df_merged[col_db].notna()
            if condition_sheet_update.any():
                update_rows = df_merged.loc[condition_sheet_update, key_columns + [col_db]].copy()
                update_rows.rename(columns={col_db: col_name}, inplace=True)
                df_sheet_updates = pd.concat([df_sheet_updates, update_rows], ignore_index=True)

        # Remove duplicates if any
        df_db_updates.drop_duplicates(inplace=True)
        df_sheet_updates.drop_duplicates(inplace=True)

        return df_db_updates, df_sheet_updates
