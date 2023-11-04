

import pandas as pd
import pickle
import os
from .model_beta import NB

REAL_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '..'))

class MlApi():
    def __init__(self):
        self._model = None

    def predict(self, data: pd.DataFrame):
        data = data.fillna('') 
        X_numeric = data.select_dtypes(include=['float']).to_numpy()
        X_string = data.select_dtypes(include=['object']).to_numpy()
        return self._model.predict(X_string, X_numeric)


    def load_model(self, name: str):
        with open(f'{REAL_PATH}/_model_{name}.pkl', 'rb') as f:
            model = pickle.load(f)
        self._model = model


    def train_new_model(self, data:pd.DataFrame, target_col:str, name='dev'):

        data = data.loc[data[target_col].notnull()] # All rows must have a target
        data = data.fillna('') 
        X_numeric = data.select_dtypes(include=['float']).to_numpy()
        X_string = data.drop(target_col, axis=1).select_dtypes(include=['object']).to_numpy()
        y = data[target_col].to_numpy()

        model = NB()
        model.fit(X_string, X_numeric, y)
        with open(f'{REAL_PATH}/_model_{name}.pkl', 'wb') as f:
            pickle.dump(model, f)