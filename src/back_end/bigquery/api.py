

import pandas as pd

class BqApi():

    def get_latest_data(self, tabel: str, project: str):
        sql = f"""
            SELECT
            MAX(date) as max_date
            FROM {tabel}
            """
        df = self.pull_pd_from_bq(sql=sql, project=project)
        return df['max_date'].values

    def push_pd_to_bq(self, df: pd.DataFrame, tabel: str, project: str, mode: str = 'append'):
        df.to_gbq(destination_table=tabel, if_exists=mode, project_id=project)
        
    def pull_pd_from_bq(self, sql: str, project: str):
        df = pd.read_gbq(sql, dialect='standard', project_id=project, progress_bar_type='tqdm')
        return df
