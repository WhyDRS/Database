import pandas as pd

class DataMerger:
    def merge_dataframes(self, df_sheet, df_db):
        columns = ['CIK', 'Ticker', 'Exchange', 'CompanyNameIssuer', 'TransferAgent', 'OnlinePurchase', 'DTCMemberNum', 'TAURL',
                   'TransferAgentPct', 'IREmails', 'IRPhoneNum', 'IRCompanyAddress', 'IRURL', 'IRContactInfo',
                   'SharesOutstanding', 'CUSIP', 'CompanyInfoURL', 'CompanyInfo', 'FullProgressPct', 'DRS',
                   'PercentSharesDRSd', 'SubmissionReceived', 'TimestampsUTC', 'LearnMoreAboutDRS', 'CertificatesOffered',
                   'SandP500', 'IncorporatedIn']

        df_sheet = df_sheet.reindex(columns=columns)
        df_db = df_db.reindex(columns=columns)

        df_sheet.replace('', pd.NA, inplace=True)
        df_db.replace('', pd.NA, inplace=True)

        df_merged = pd.merge(df_sheet, df_db, on=['CIK', 'Ticker'], how='outer', suffixes=('_sheet', '_db'), indicator=True)

        df_db_updates = pd.DataFrame()
        df_sheet_updates = pd.DataFrame()

        for col in columns:
            if col in ['CIK', 'Ticker']:
                continue
            col_sheet = col + '_sheet'
            col_db = col + '_db'

            condition_db_update = df_merged[col_db].isna() & df_merged[col_sheet].notna()
            df_db_updates.loc[condition_db_update, col] = df_merged.loc[condition_db_update, col_sheet]

            condition_sheet_update = df_merged[col_sheet].isna() & df_merged[col_db].notna()
            df_sheet_updates.loc[condition_sheet_update, col] = df_merged.loc[condition_sheet_update, col_db]

        df_db_updates[['CIK', 'Ticker']] = df_merged.loc[df_db_updates.index, ['CIK', 'Ticker']]
        df_sheet_updates[['CIK', 'Ticker']] = df_merged.loc[df_sheet_updates.index, ['CIK', 'Ticker']]

        return df_db_updates, df_sheet_updates
