

import json
import os
import sys
import pandas as pd

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    BASE_PATH = sys._MEIPASS
except Exception:
    BASE_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '..'))
TRANS_FILE = '_categories.json'
ASSETS_FILE = '_assets.json'


class CategoriesApi():
    def get_transaction_list(self) -> list:
        with open(f'{BASE_PATH}/{TRANS_FILE}') as f:
            categories = json.load(f)
        categories_dict = {key: value['prior'] for key, value in categories.items()}
        categories_sorted = {k: v for k, v in sorted(categories_dict.items(), key=lambda item: item[1], reverse=True)}
        return categories_sorted.keys()
    
    def get_assets_list(self) -> list:
        with open(f'{BASE_PATH}/{ASSETS_FILE}') as f:
            categories = json.load(f)
        categories_dict = {key: value['order'] for key, value in categories.items()}
        categories_sorted = {k: v for k, v in sorted(categories_dict.items(), key=lambda item: item[1])}
        return categories_sorted.keys()
    
    def get_assets_list_explanations(self) -> list:
        with open(f'{BASE_PATH}/{ASSETS_FILE}') as f:
            categories = json.load(f)
        categories_dict = {key: value['order'] for key, value in categories.items()}
        categories_sorted = {k: v for k, v in sorted(categories_dict.items(), key=lambda item: item[1])}
        return [categories[key]['explanation'] for key in categories_sorted]
    
    def get_assets_df(self):
        df = pd.DataFrame(columns=['date', 'category', 'explanation', 'value'])
        df['category'] = self.get_assets_list()
        df['explanation'] = self.get_assets_list_explanations()
        df = df.astype({'date': 'str'})
        df = df.astype({'category': 'str'})
        df = df.astype({'explanation': 'str'})
        df = df.astype({'value': 'float'})
        return df
    
    def update_assets_list_order(self, new_data: dict):
        with open(f'{BASE_PATH}/{ASSETS_FILE}') as f:
            old_data = json.load(f)
        for key, value in new_data.items():
            old_data[key]['order'] = value
        with open(f'{BASE_PATH}/{ASSETS_FILE}', 'w', encoding='utf-8') as f:
            json.dump(old_data , f, ensure_ascii=False, indent=4) 

    def update_transaction_list_order(self, new_data: dict):
        with open(f'{BASE_PATH}/{TRANS_FILE}') as f:
            old_data = json.load(f)
        for key, value in new_data.items():
            old_data[key]['prior'] = value
        with open(f'{BASE_PATH}/{TRANS_FILE}', 'w', encoding='utf-8') as f:
            json.dump(old_data , f, ensure_ascii=False, indent=4) 

    
    def add_asset(self, name: str, explanation: str):
        data = {f'{name}':
                    {
                    'explanation': explanation,
                    'order': 99,
                    }
                }
        with open(f'{BASE_PATH}/{ASSETS_FILE}') as f:
            old_data = json.load(f)
        data.update(old_data)
        with open(f'{BASE_PATH}/{ASSETS_FILE}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_transaction(self, name: str):
        data = {f'{name}': {'prior': 0.00}}
        with open(f'{BASE_PATH}/{TRANS_FILE}') as f:
            old_data = json.load(f)
        data.update(old_data)
        with open(f'{BASE_PATH}/{TRANS_FILE}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4) 
    
    def remove_asset(self, name: str):
        self._remove_data(name=name, filename=ASSETS_FILE)

    def remove_transaction(self, name: str):
        self._remove_data(name=name, filename=TRANS_FILE)

    def _remove_data(self, name: str, filename: str) -> None:
        with open(f'{BASE_PATH}/{filename}') as f:
            old_data = json.load(f)
        old_data.pop(name, None)
        with open(f'{BASE_PATH}/{filename}', 'w', encoding='utf-8') as f:
            json.dump(old_data, f, ensure_ascii=False, indent=4)
