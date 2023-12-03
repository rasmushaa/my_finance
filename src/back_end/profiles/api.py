

import json
import os
import sys
from .user import User
from src.back_end.categories import CategoriesApi
from src.back_end.ml import MlApi


try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    BASE_PATH = sys._MEIPASS
except Exception:
    BASE_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '..'))
FILE_NAME = 'profiles.json'


class ProfileApi():

    def get_profile_names(self):
        profiles = self._load_profiles_json()
        if profiles:
            return [name for name in profiles]
        else:
            return [None]
    
    def get_user_class(self, target_name: str):
        profiles = self._load_profiles_json()
        for name in profiles:
            if name == target_name:
                return User(name=name, 
                            bq_project=profiles[name]['bq_project'],
                            table_transactions=profiles[name]['table_transactions'],
                            table_assets=profiles[name]['table_assets']
                            )
        return None
            
    def add_profile(self, name: str, bq_project: str, table_transactions: str, table_assets: str):
        assert '.' in table_transactions, 'Transaction table must include dataset name ("." notation)'
        assert '.' in table_assets, 'Assets table must include dataset name ("." notation)'

        data = {f'{name}':
                    {
                    'bq_project': bq_project,
                    'table_transactions': table_transactions,
                    'table_assets': table_assets
                    }
                }
        profiles = self._load_profiles_json()
        data.update(profiles)
        with open(f'{BASE_PATH}/{FILE_NAME}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def remove_profile(self, target_name: str):
        profiles = self._load_profiles_json()
        profiles.pop(target_name, None)
        with open(f'{BASE_PATH}/{FILE_NAME}', 'w', encoding='utf-8') as f:
            json.dump(profiles, f, ensure_ascii=False, indent=4)
        CategoriesApi()._delete_user_data(user_name=target_name)
        MlApi()._delete_user_data(user_name=target_name)
        

    def _load_profiles_json(self):
        try:
            with open(f'{BASE_PATH}/{FILE_NAME}') as f:
                profiles = json.load(f)
        except FileNotFoundError:
            profiles = {}
        return profiles