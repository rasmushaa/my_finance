

class User():
    def __init__(self, name: str, bq_project: str, table_transactions: str, table_assets: str):
        self.name = name
        self.bq_project = bq_project
        self.table_transactions = table_transactions
        self.table_assets = table_assets