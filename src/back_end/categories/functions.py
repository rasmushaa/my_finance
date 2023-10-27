

import pandas as pd
import chardet
import csv
import json
import os


REAL_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '..'))


def get_transaction_list() -> list:
    with open(f'{REAL_PATH}/_categories.json') as f:
        categories = json.load(f)
    return [name for name in categories]
