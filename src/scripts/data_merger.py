import pandas as pd

class DataMerger:
    def merge_dataframes(self, df_sheet, df_db):
        # Define the columns of interest (first 27 columns)
        columns = [
            'Ticker', 'Exchange', 'CompanyNameIssuer', 'TransferAgent', 'OnlinePurchase', 'DTCMemberNum', 'TAURL',
            'TransferAgentPct', 'IREmails', 'IRPhoneNum', 'IRCompanyAddress', 'IRURL', 'IRContactInfo',
            'SharesOutstanding', 'CUSIP', 'CompanyInfoURL', 'CompanyInfo', 'FullProgressPct', 'CIK', 'DRS',
            'PercentSharesDRSd', 'SubmissionReceived', 'TimestampsUTC', 'LearnMoreAboutDRS', 'CertificatesOffered',
            'SandP500', 'IncorporatedIn'
        ]

        # Ensure the DataFrames have the correct columns
        df_sheet = df_sheet.reindex(columns=columns)
        df_db = df_db.reindex(columns=columns)

        df_sheet.replace(['', ' '], pd.NA, inplace=True)
        df_db.replace(['', ' '], pd.NA, inplace=True)

        # Merge on three keys: CIK, Ticker, CompanyNameIssuer
        df_merged = pd.merge(
            df_sheet, df_db,
            on=['CIK', 'Ticker', 'CompanyNameIssuer'],
            how='outer',
            suffixes=('_sheet', '_db'),
            indicator=True
        )

        df_db_updates = pd.DataFrame()
        df_sheet_updates = pd.DataFrame()

        for col in columns:
            if col in ['CIK', 'Ticker', 'CompanyNameIssuer']:
                continue
            col_sheet = col + '_sheet'
            col_db = col + '_db'

            # Update database where DB has NaN and sheet has data
            condition_db_update = df_merged[col_db].isna() & df_merged[col_sheet].notna()
            updates_db = df_merged.loc[condition_db_update, ['CIK', 'Ticker', 'CompanyNameIssuer', col_sheet]].rename(columns={col_sheet: col})
            df_db_updates = pd.concat([df_db_updates, updates_db], ignore_index=True)

            # Update sheet where sheet has NaN and DB has data
            condition_sheet_update = df_merged[col_sheet].isna() & df_merged[col_db].notna()
            updates_sheet = df_merged.loc[condition_sheet_update, ['CIK', 'Ticker', 'CompanyNameIssuer', col_db]].rename(columns={col_db: col})
            df_sheet_updates = pd.concat([df_sheet_updates, updates_sheet], ignore_index=True)

        # Remove duplicates in updates
        df_db_updates = df_db_updates.drop_duplicates(subset=['CIK', 'Ticker', 'CompanyNameIssuer', col])
        df_sheet_updates = df_sheet_updates.drop_duplicates(subset=['CIK', 'Ticker', 'CompanyNameIssuer', col])

        return df_db_updates, df_sheet_updates
