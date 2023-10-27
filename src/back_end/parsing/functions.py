

import pandas as pd
import chardet
import csv
import json
import os


REAL_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '..'))


def csv_to_pandas(path: str):
    if not path.endswith('.csv'):
        raise TypeError("File type is not supported!\nOnly CSV files are allowed...") 
    
    encoding, separator = _detect_file_coding(path)
    df = pd.read_csv(path, encoding=encoding, sep=separator)
    return df


def pandas_in_known_files(df: pd.DataFrame) -> bool:
    with open(f'{REAL_PATH}/_file_types.json') as f:
        file_types = json.load(f)
    for name in file_types:
        if sorted(df.columns.values.tolist()) == sorted(file_types[name]['columns']):
            return True
    return False


def add_pandas_to_known_files(df: pd.DataFrame, name: str, date_column: str, date_format: str, amount_column: str, receiver_column: str):
    data = {f'{name}':
                {
                'columns': df.columns.values.tolist(), 
                'date_column': date_column,
                'date_format': date_format, 
                'amount_column': amount_column, 
                'receiver_column': receiver_column
                }
            }
    with open(f'{REAL_PATH}/_file_types.json') as f:
        old_data = json.load(f)
    data.update(old_data)
    with open(f'{REAL_PATH}/_file_types.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def process_pandas(df: pd.DataFrame) -> pd.DataFrame:
    df_temp = df.copy()
    if pandas_in_known_files(df_temp):
        file_type = get_pandas_file_type(df_temp)
        df_temp = df_temp[[file_type['date_column'], file_type['receiver_column'], file_type['amount_column']]]
        df_temp = df_temp.rename({file_type['date_column']: 'Date',
                                  file_type['receiver_column']: 'Receiver', 
                                  file_type['amount_column']: 'Amount'}, axis=1) 
        df_temp['Date'] = pd.to_datetime(df_temp['Date'], format=file_type['date_format'])
        df_temp['Date'] = df_temp['Date'].dt.date.astype(str)
        df_temp['Amount'] = df_temp['Amount'].astype(str).str.replace(',', '.')
        df_temp = df_temp.astype({'Amount': 'float'})
        df_temp = df_temp.astype({'Receiver': 'str'})
        df_temp['Category'] = ''
        df_temp = df_temp.astype({'Category': 'str'})
        df_temp = df_temp.fillna("")    
        return df_temp
    else:
        return df_temp
    

def get_pandas_file_type(df: pd.DataFrame) -> json:
    with open(f'{REAL_PATH}/_file_types.json') as f:
        file_types = json.load(f)
    for name in file_types:
        if sorted(df.columns.values.tolist()) == sorted(file_types[name]['columns']):
            return file_types[name]
        

def _detect_file_coding(path: str) -> str:
    with open(path, 'rb') as csv_file:
        encoding_dict = chardet.detect(csv_file.read())
        encoding = encoding_dict['encoding']
    with open(path, 'r', encoding=encoding) as csv_file:
        dialect = csv.Sniffer().sniff(csv_file.read(), delimiters=[',', ';', '', '\t', '|'])
        separator = dialect.delimiter
    return encoding, separator
    

