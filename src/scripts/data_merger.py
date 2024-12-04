import pandas as pd

class DataMerger:
    def merge_dataframes(self, df_sheet, df_db):
        # We only consider the first 27 columns
        df_sheet = df_sheet.iloc[:, :27]
        df_db = df_db.iloc[:, :27]

        # Replace empty strings with NaN for comparison
        df_sheet.replace('', pd.NA, inplace=True)
        df_db.replace('', pd.NA, inplace=True)

        # Merge on composite key (CIK, Ticker, CompanyNameIssuer)
        df_merged = pd.merge(
            df_sheet, df_db,
            left_on=[df_sheet.columns[18], df_sheet.columns[0], df_sheet.columns[2]],
            right_on=[df_db.columns[18], df_db.columns[0], df_db.columns[2]],
            how='outer',
            suffixes=('_sheet', '_db'),
            indicator=True
        )

        df_db_updates = pd.DataFrame()
        df_sheet_updates = pd.DataFrame()

        for i in range(27):
            if i in [0, 2, 18]:  # Skip keys
                continue
            col_sheet = df_sheet.columns[i] + '_sheet'
            col_db = df_db.columns[i] + '_db'

            # Update database where DB has NaN and sheet has data
            condition_db_update = df_merged[col_db].isna() & df_merged[col_sheet].notna()
            df_db_updates.loc[condition_db_update, i] = df_merged.loc[condition_db_update, col_sheet]

            # Update sheet where sheet has NaN and DB has data
            condition_sheet_update = df_merged[col_sheet].isna() & df_merged[col_db].notna()
            df_sheet_updates.loc[condition_sheet_update, i] = df_merged.loc[condition_sheet_update, col_db]

        # Include primary keys
        df_db_updates[0] = df_merged[df_sheet.columns[0] + '_sheet']
        df_db_updates[2] = df_merged[df_sheet.columns[2] + '_sheet']
        df_db_updates[18] = df_merged[df_sheet.columns[18] + '_sheet']

        df_sheet_updates[0] = df_merged[df_sheet.columns[0] + '_sheet']
        df_sheet_updates[2] = df_merged[df_sheet.columns[2] + '_sheet']
        df_sheet_updates[18] = df_merged[df_sheet.columns[18] + '_sheet']

        # Reorder columns
        df_db_updates = df_db_updates.sort_index(axis=1)
        df_sheet_updates = df_sheet_updates.sort_index(axis=1)

        return df_db_updates, df_sheet_updates
