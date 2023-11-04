

import json
import os

REAL_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '..'))


class CategoriesApi():
    def get_transaction_list(self) -> list:
        with open(f'{REAL_PATH}/_categories.json') as f:
            categories = json.load(f)
        return [name for name in categories]
