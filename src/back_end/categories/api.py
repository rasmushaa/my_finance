

import json
import os
import sys

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    BASE_PATH = sys._MEIPASS
except Exception:
    BASE_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '..'))

FILE_NAME = '_categories.json'


class CategoriesApi():
    def get_transaction_list(self) -> list:
        with open(f'{BASE_PATH}/{FILE_NAME}') as f:
            categories = json.load(f)
        return [name for name in categories]
