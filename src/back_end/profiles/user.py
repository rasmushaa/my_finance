

class User():
    def __init__(self, name: str, bq_account: str, bq_project: str, table_transactions: str, table_assets: str):
        self.name = name
        self.bq_account = bq_account
        self.bq_project = bq_project
        self.dataset = table_transactions.split('.')[0]
        self.table_transactions = table_transactions.split('.')[1]
        self.table_assets = table_assets.split('.')[1]