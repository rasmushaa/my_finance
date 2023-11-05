

import json
from .user import User
import os
import sys

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    BASE_PATH = sys._MEIPASS
except Exception:
    BASE_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '..'))

FILE_NAME = '_profiles.json'


class ProfileApi():

    def get_profile_names(self):
        profiles = self._load_profiles_json()
        if profiles is not None:
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
        return [None]
            
    def add_profile(self, name: str, bq_project: str, table_transactions: str, table_assets: str):
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

    def _load_profiles_json(self):
        try:
            with open(f'{BASE_PATH}/{FILE_NAME}') as f:
                profiles = json.load(f)
        except FileNotFoundError:
            profiles = None
        return profiles