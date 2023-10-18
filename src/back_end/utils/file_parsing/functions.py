

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


def add_pandas_to_known_files(df: pd.DataFrame, date_column: int, amount_column: int, receiver_column: int, name: str):
    data = {f'{name}':
                {
                'columns': df.columns.values.tolist(), 
                'date_column': date_column, 
                'amount_column': amount_column, 
                'receiver_column': receiver_column
                }
            }
    with open(f'{REAL_PATH}/_file_types.json') as f:
        old_data = json.load(f)
    data.update(old_data)
    with open(f'{REAL_PATH}/_file_types.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def _detect_file_coding(path: str) -> str:
    with open(path, 'rb') as csv_file:
        encoding_dict = chardet.detect(csv_file.read())
        encoding = encoding_dict['encoding']
    with open(path, 'r', encoding=encoding) as csv_file:
        dialect = csv.Sniffer().sniff(csv_file.read(), delimiters=[',', ';', '', '\t', '|'])
        separator = dialect.delimiter
    return encoding, separator
    




def _detect_bank(self, df: type[pd.DataFrame]) -> str:
    
    column_list = list(df.columns)

    if (len(column_list) == 4 and
        column_list[0] == 'Date' and
        column_list[1] == 'Receiver' and
        column_list[2] == 'Amount' and
        column_list[3] == 'Category'):
        return 'AIDF'
    
    elif (len(column_list) == 7 and
        column_list[0] == 'Date' and
        column_list[1] == 'Receiver' and
        column_list[2] == 'Amount' and
        column_list[3] == 'Category' and 
        column_list[4] == 'Category ID' and
        column_list[5] == 'Commit date' and
        column_list[6] == 'Commit file ID'):
        return 'AIDF_GS'
    
    elif (len(column_list) == 5 and
        column_list[0] == 'Päivämäärä' and
        column_list[1] == 'Saaja/Maksaja' and
        column_list[2] == 'Selite' and
        column_list[3] == 'Viite/Viesti' and
        column_list[4] == 'Määrä'):
        return 'POP_HB'
    
    elif (len(column_list) == 11 and
        column_list[0] == 'Kirjauspäivä' and
        column_list[1] == 'Arvopäivä' and
        column_list[2] == 'Määrä EUROA' and
        column_list[3] == 'Laji' and
        column_list[4] == 'Selitys' and
        column_list[5] == 'Saaja/Maksaja' and
        column_list[6] == 'Saajan tilinumero' and
        column_list[7] == 'Saajan pankin BIC' and
        column_list[8] == 'Viite' and
        column_list[9] == 'Viesti' and
        column_list[10] == 'Arkistointitunnus'):
        return 'OP'
    
    #elif (Your file detection code):
        #return 'YourBankCSV'       
    else:
        raise TypeError("The Bank is not supported...")
    
                
def _transform2aidf(self, df: type[pd.DataFrame], bank_file_type : str) -> type[pd.DataFrame]:                      
    if bank_file_type == 'AIDF':
        df = df.fillna("")
        
    elif bank_file_type == 'AIDF_GS':
        df = df.drop(['Category ID', 'Commit date', 'Commit file ID'], axis=1)
        df = df.astype({'Date':'string','Receiver':'string','Amount':'float','Category':'string'})
        df = df.fillna("")
    
    elif bank_file_type == 'POP_HB':       
        df = df.rename({'Päivämäärä': 'Date', 
                        'Saaja/Maksaja': 'Receiver', 
                        'Määrä': 'Amount'}, axis=1)      
        df = df.drop(['Selite', 'Viite/Viesti'], axis=1)
        df["Category"] = ""
        df['Amount'] = df['Amount'].astype(str).str.replace(',', '.')
        df = df.astype({'Amount': 'float'})
        df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
        df['Date'] = df['Date'].dt.date.astype(str)
        df = df.fillna("")       

    elif bank_file_type == 'OP':       
        df = df.rename({'Kirjauspäivä': 'Date', 
                        'Saaja/Maksaja': 'Receiver', 
                        'Määrä EUROA': 'Amount'}, axis=1)      
        df = df.drop(['Arvopäivä', 
                        'Laji',
                        'Selitys',
                        'Saajan tilinumero',
                        'Saajan pankin BIC',
                        'Viite',
                        'Viesti',
                        'Arkistointitunnus'], axis=1)
        df["Category"] = ""
        df['Amount'] = df['Amount'].astype(str).str.replace(',', '.')
        df = df.astype({'Amount': 'float'})
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
        df['Date'] = df['Date'].dt.date.astype(str)
        df = df.fillna("")      
        df = df[['Date', 'Receiver', 'Amount', 'Category']]
    
    #if file_type == 'YourBankCSV':
        #Your transform code goes here...         
    return df