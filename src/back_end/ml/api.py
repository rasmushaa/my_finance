

import pandas as pd
import pickle
from .model_delta import NB
import os
import sys

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    BASE_PATH = sys._MEIPASS
except Exception:
    BASE_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '..'))
FILE_NAME = 'model'


class MlApi():
    def __init__(self):
        self._model = None

    def predict(self, data: pd.DataFrame):
        data = data.fillna('') 
        X_numeric = data.select_dtypes(include=['float']).to_numpy()
        X_string = data.select_dtypes(include=['object']).to_numpy()
        if self._model is not None:
            return self._model.predict(X_string, X_numeric)
        else:
            return [{'': 1}]


    def load_model(self, name: str):
        self._model = None
        with open(f'{BASE_PATH}/{name}_{FILE_NAME }.pkl', 'rb') as f:
            model = pickle.load(f)
        self._model = model
        
    
    def get_propabilities(self, name: str):
        self.load_model(name)
        return self._model.get_priors()


    def train_new_model(self, data:pd.DataFrame, target_col:str, name='dev'):

        data = data.loc[data[target_col].notnull()] # All rows must have a target
        data = data.fillna('') 
        X_numeric = data.select_dtypes(include=['float']).to_numpy()
        X_string = data.drop(target_col, axis=1).select_dtypes(include=['object']).to_numpy()
        y = data[target_col].to_numpy()

        model = NB()
        model.fit(X_string, X_numeric, y)
        with open(f'{BASE_PATH}/{name}_{FILE_NAME }.pkl', 'wb') as f:
            pickle.dump(model, f)