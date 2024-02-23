

import json
import os
import sys
import pandas as pd
from datetime import datetime

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    BASE_PATH = sys._MEIPASS
except Exception:
    BASE_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '..'))
TRANS_FILE = 'categories.json'
ASSETS_FILE = 'assets.json'


class CategoriesApi():
    def get_transaction_list(self, user_name: str) -> list:
        categories = self._load_data(filename=f'{user_name}_{TRANS_FILE}')
        if categories:
            categories_sorted = self._sort_json(categories, order_key='prior', reverse=True)
            return categories_sorted.keys()
        return ['empty']
        

    def get_assets_list(self, user_name: str)  -> list:
        categories = self._load_data(filename=f'{user_name}_{ASSETS_FILE}')
        if categories:
            categories_sorted = self._sort_json(categories, order_key='order', reverse=False)
            return categories_sorted.keys()
        return ['empty']
    

    def get_assets_list_explanations(self, user_name: str)  -> list:
        categories = self._load_data(filename=f'{user_name}_{ASSETS_FILE}')
        if categories:
            categories_sorted = self._sort_json(categories, order_key='order', reverse=False)
            return [categories[key]['explanation'] for key in categories_sorted]
        return ['empty']
    

    def get_assets_df(self, user_name: str):
        df = pd.DataFrame()
        df['category'] = self.get_assets_list(user_name=user_name)
        df['explanation'] = self.get_assets_list_explanations(user_name=user_name)
        df['date'] = datetime.today().strftime('%Y-%m-%d')
        df['value'] = 0.0
        df = df.astype({'category': 'str'})
        df = df.astype({'explanation': 'str'})
        df = df.astype({'date': 'str'})
        df = df.astype({'value': 'float'})
        df = df[['date', 'category', 'explanation', 'value']]
        return df
    

    def update_assets_list_order(self, new_data: dict, user_name: str):
        old_data = self._load_data(filename=f'{user_name}_{ASSETS_FILE}')
        for key, value in new_data.items():
            old_data[key]['order'] = value
        self._dump_data(old_data, filename=f'{user_name}_{ASSETS_FILE}')


    def update_transaction_list_order(self, new_data: dict, user_name: str):
        old_data = self._load_data(filename=f'{user_name}_{TRANS_FILE}')
        for key, value in new_data.items():
            old_data[key]['prior'] = value
        self._dump_data(old_data, filename=f'{user_name}_{TRANS_FILE}')

    
    def add_asset(self, name: str, explanation: str, user_name: str):
        data = {f'{name}':
                    {
                    'explanation': explanation,
                    'order': 99, # Asset list is sorted by computed place, and for new categories it's 99 ("large")
                    }
                }
        old_data = self._load_data(filename=f'{user_name}_{ASSETS_FILE}')
        data.update(old_data)
        self._dump_data(data, filename=f'{user_name}_{ASSETS_FILE}')


    def add_transaction(self, name: str, user_name: str):
        data = {f'{name}': {'prior': 0.00}} # Transaction list is sorted by computed prior, and for new categories it's zero
        old_data = self._load_data(filename=f'{user_name}_{TRANS_FILE}')
        data.update(old_data)
        self._dump_data(data, filename=f'{user_name}_{TRANS_FILE}')
    

    def remove_asset(self, name: str, user_name: str):
        self._remove_data(name=name, filename=f'{user_name}_{ASSETS_FILE}')


    def remove_transaction(self, name: str, user_name: str):
        self._remove_data(name=name, filename=f'{user_name}_{TRANS_FILE}')


    def _remove_data(self, name: str, filename: str) -> None:
        old_data = self._load_data(filename=filename)
        old_data.pop(name, None)
        self._dump_data(old_data, filename=filename)

    def _delete_user_data(self, user_name: str) -> None:
        user_file = f'{BASE_PATH}/{user_name}_{ASSETS_FILE}'
        if os.path.isfile(user_file):
            os.remove(user_file)
        user_file = f'{BASE_PATH}/{user_name}_{TRANS_FILE}'
        if os.path.isfile(user_file):
            os.remove(user_file)


    def _sort_json(self, json_dict: dict, order_key: str, reverse: bool = False):
        dict_values = {key: value[order_key] for key, value in json_dict.items()}
        sorted_dict = {k: v for k, v in sorted(dict_values.items(), key=lambda item: item[1], reverse=reverse)}
        return sorted_dict


    def _dump_data(self, data: dict, filename: str):
        with open(f'{BASE_PATH}/{filename}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def _load_data(self, filename: str) -> dict:
        try:
            with open(f'{BASE_PATH}/{filename}') as f:
                json_dict = json.load(f)
        except FileNotFoundError:
            json_dict = {}
        return json_dict
