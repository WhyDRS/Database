import pandas as pd

class DataMerger:
    def merge_dataframes(self, df_sheet, df_db):
        # We only consider the first 27 columns
        df_sheet = df_sheet.iloc[:, :27].copy()
        df_db = df_db.iloc[:, :27].copy()

        # Rename columns to standard names
        col_names = [f'col{i}' for i in range(27)]
        df_sheet.columns = col_names
        df_db.columns = col_names

        # Replace empty strings with NaN for comparison
        df_sheet.replace('', pd.NA, inplace=True)
        df_db.replace('', pd.NA, inplace=True)

        # Merge on composite key (CIK, Ticker, CompanyNameIssuer)
        key_columns = ['col18', 'col0', 'col2']  # CIK, Ticker, CompanyNameIssuer
        df_merged = pd.merge(
            df_sheet, df_db,
            on=key_columns,
            how='outer',
            suffixes=('_sheet', '_db'),
            indicator=True
        )

        df_db_updates = pd.DataFrame()
        df_sheet_updates = pd.DataFrame()

        for i in range(27):
            col_name = f'col{i}'
            if col_name in key_columns:
                continue
            col_sheet = f'{col_name}_sheet'
            col_db = f'{col_name}_db'

            # Update database where DB has NaN and sheet has data
            condition_db_update = df_merged[col_db].isna() & df_merged[col_sheet].notna()
            if condition_db_update.any():
                df_db_updates = pd.concat([df_db_updates, df_merged.loc[condition_db_update, key_columns + [col_sheet]]])

            # Update sheet where sheet has NaN and DB has data
            condition_sheet_update = df_merged[col_sheet].isna() & df_merged[col_db].notna()
            if condition_sheet_update.any():
                df_sheet_updates = pd.concat([df_sheet_updates, df_merged.loc[condition_sheet_update, key_columns + [col_db]]])

        # Rename columns back to standard names
        if not df_db_updates.empty:
            df_db_updates.rename(columns={f'col{i}_sheet': f'col{i}' for i in range(27)}, inplace=True)
            df_db_updates.drop_duplicates(inplace=True)

        if not df_sheet_updates.empty:
            df_sheet_updates.rename(columns={f'col{i}_db': f'col{i}' for i in range(27)}, inplace=True)
            df_sheet_updates.drop_duplicates(inplace=True)

        return df_db_updates, df_sheet_updates
