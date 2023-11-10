

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
        table_schema = [] # [{'name': 'col1', 'type': 'STRING'},...]
        for col in df.columns:
            if 'date' in col.lower():
                 table_schema.append({'name': col, 'type': 'DATE'})
            elif 'object' in str(df[col].dtype):
                 table_schema.append({'name': col, 'type': 'STRING'})
            elif 'float' in str(df[col].dtype):
                table_schema.append({'name': col, 'type': 'FLOAT64'})
            elif 'datetime' in str(df[col].dtype):
                table_schema.append({'name': col, 'type': 'TIMESTAMP'})
        df.to_gbq(destination_table=tabel, 
                  if_exists=mode, 
                  project_id=project, 
                  table_schema=table_schema, 
                  location='europe-north1')
        
    def pull_pd_from_bq(self, sql: str, project: str):
        df = pd.read_gbq(sql, dialect='standard', project_id=project, location='europe-north1')
        return df
