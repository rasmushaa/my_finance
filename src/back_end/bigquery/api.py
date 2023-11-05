

import pandas as pd

class BqApi():
    def get_latest_date(self, tabel: str, project: str):
        sql = f"""
            SELECT
            date
            FROM {tabel}
            GROUP BY date
            """
        try:
            df = self.pull_pd_from_bq(sql=sql, project=project)
            return pd.to_datetime(df['date'].max(), format='%Y-%m-%d')
        except:
            return pd.to_datetime('2000-01-01', format='%Y-%m-%d')

    def push_pd_to_bq(self, df: pd.DataFrame, tabel: str, project: str, mode: str = 'append'):
        df = df.copy()
        df['commit_timestamp'] = pd.Timestamp('now', tz='Europe/Helsinki')
        df.to_gbq(destination_table=tabel, if_exists=mode, project_id=project, location='europe-north1')
        
    def pull_pd_from_bq(self, sql: str, project: str):
        df = pd.read_gbq(sql, dialect='standard', project_id=project, location='europe-north1')
        return df
