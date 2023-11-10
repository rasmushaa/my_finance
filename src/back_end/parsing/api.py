

import pandas as pd
import chardet
import csv
import json
import os
import sys

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    BASE_PATH = sys._MEIPASS
except Exception:
    BASE_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '..'))
FILE_NAME = '_file_types.json'


class FileParsingApi():
    def get_known_files(self) -> list[str]:
        ''' Returns a list names of known files.
        Returns
        -------
        List : str
            A list containing all known file names.
            If stored names file is empty, then returns None
        '''
        with open(f'{BASE_PATH}/{FILE_NAME}') as f:
            file_types = json.load(f)
        if len(file_types) > 0:
            return [ftype for ftype in file_types]
        else:
            return [None]

    def csv_to_pandas(self, path: str) -> pd.DataFrame:
        ''' Automatically converts CSV files to pandas

        By default, pandas is unable to detect used encoding,
        and sepeparators of given files. Thus, it has to be
        done manually.

        Parameters
        ----------
        path : str
            An absolute path to the file to convert
        
        Returns
        -------
        df : pd.DataFrame
            A correclty opened csv file in pandas format.
        None : None
            If given file is not a csv, an errro is thrown.
        '''
        if path.endswith('.csv'):
            encoding, separator = self._detect_file_coding(path)
            df = pd.read_csv(path, encoding=encoding, sep=separator)
            return df
        else:
            raise TypeError("File type is not supported!\nOnly CSV files are allowed...") 
        

    def pandas_in_known_files(self, df: pd.DataFrame) -> bool:
        ''' Checks if given data frame is located in excisting table formats

        Tables are separated by the column names.
        The order does not matter since its sorted 
        in the comparison, but capital letters matter.

        Parameters
        ----------
        df : pd.DataFrame
            A df to be chekced

        Returns
        -------
        results : bool
            True if file is known
        '''
        with open(f'{BASE_PATH}/{FILE_NAME}') as f:
            file_types = json.load(f)
        for name in file_types:
            if sorted(df.columns.values.tolist()) == sorted(file_types[name]['columns']):
                return True
        return False
    

    def add_pandas_to_known_files(self, df: pd.DataFrame, name: str, date_column: str, date_format: str, amount_column: str, receiver_column: str):
        ''' Adds given pandas to known files.

        Tables are separated by the column names.
        The order does not matter since its sorted 
        in the comparison, but capital letters matter.

        Parameters
        ----------
        df : pd.DataFrame
            A df to be added.
        name : str
            Given filename for table, which is visible to end user.
        date_column : str
            Date column name.
        date_format : str
            User specified date format. ('YYYY-MM-DD')
        amount_column : str
            Value column name.
        receiver_column : str
            Receiver column name.
        '''
        data = {f'{name}':
                    {
                    'columns': df.columns.values.tolist(), 
                    'date_column': date_column,
                    'date_format': date_format, 
                    'amount_column': amount_column, 
                    'receiver_column': receiver_column
                    }
                }
        with open(f'{BASE_PATH}/{FILE_NAME}') as f:
            old_data = json.load(f)
        data.update(old_data)
        with open(f'{BASE_PATH}/{FILE_NAME}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def remove_known_file(self, filename: str):
        ''' Deletes an existing My Finance dataframe format.

        Parameters
        ----------
        filename : str
            Known filename to be popped out.
        '''
        with open(f'{BASE_PATH}/{FILE_NAME}') as f:
            file_types = json.load(f)
        file_types.pop(filename, None)
        with open(f'{BASE_PATH}/{FILE_NAME}', 'w', encoding='utf-8') as f:
            json.dump(file_types, f, ensure_ascii=False, indent=4)


    def process_pandas(self, df: pd.DataFrame) -> pd.DataFrame:
        ''' Transforms a input pandas to My Finance dataframe format.

        The column names and data types will affect BigQuery table,
        and Looker studio reports

        Parameters
        ----------
        df : pd.DataFrame
            A df to be processed

        Returns
        -------
        df : pd.DataFrame
            A Processed df
        '''
        df_temp = df.copy()
        if self.pandas_in_known_files(df_temp):
            file_type = self._get_pandas_file_type(df_temp)
            df_temp = df_temp[[file_type['date_column'], file_type['receiver_column'], file_type['amount_column']]]
            df_temp = df_temp.rename({file_type['date_column']: 'date',
                                    file_type['receiver_column']: 'receiver', 
                                    file_type['amount_column']: 'amount'}, axis=1)
            df_temp['date'] = pd.to_datetime(df_temp['date'], format=file_type['date_format'])
            df_temp = df_temp.astype({'date': 'str'})
            df_temp['amount'] = df_temp['amount'].astype(str).str.replace(',', '.')
            df_temp = df_temp.astype({'amount': 'float'})
            df_temp = df_temp.astype({'receiver': 'str'})
            df_temp['category'] = ''
            df_temp = df_temp.astype({'category': 'str'})
            df_temp = df_temp.fillna("")    
            return df_temp
        else:
            return df_temp
        

    def _get_pandas_file_type(self, df: pd.DataFrame) -> json:
        ''' Loads an existing pandas file parsing json.

        The file contains the names of required columns.

        Parameters
        ----------
        df : pd.DataFrame
            A df to be looked for.

        Returns
        -------
        File : dict
            Json dict containing information about the df.
        '''
        with open(f'{BASE_PATH}/{FILE_NAME}') as f:
            file_types = json.load(f)
        for name in file_types:
            if sorted(df.columns.values.tolist()) == sorted(file_types[name]['columns']):
                return file_types[name]
        

    def _detect_file_coding(self, path: str) -> str:
        ''' Auto detects used encoding and separator in csv file.

        If file parameters are unkwown, it has to be first opened in binary
        to avoid any parsing errors.

        Parameters
        ----------
        path : str
            An absolute path to the file to convert

        Returns
        -------
        encoding : str
            Detected encoding. Note, chardet works well, but its not perfect!
        separator : str
            Detected separator in [',', ';', '', '\t', '|']
        '''
        with open(path, 'rb') as csv_file:
            encoding_dict = chardet.detect(csv_file.read())
            encoding = encoding_dict['encoding']
        with open(path, 'r', encoding=encoding) as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.read(), delimiters=[',', ';', '', '\t', '|'])
            separator = dialect.delimiter
        return encoding, separator