

from PyQt5 import QtWidgets
from PyQt5 import Qt
from PyQt5 import QtCore
import pandas as pd
from .dialog import FileParsingDialog
from .table import FinanceTableView
from src.back_end import parsing
from src.back_end.bigquery import BqApi
from src.back_end.profiles import ProfileApi
from src.front_end.utils import Message


class TabTransaction(QtWidgets.QWidget):
    def __init__(self, parent:object):
        super().__init__()
        self._init_window()
        self.setAcceptDrops(True)

    
    def _init_window(self):
        grid = QtWidgets.QGridLayout() 
        # User
        self._user_name = QtWidgets.QLabel()
        self._user_name.setText('<user_name>')
        grid.addWidget(self._user_name, 0, 0, 1, 1)
        grid.setColumnStretch(0, 1)
        # Push button
        self._start_button = QtWidgets.QPushButton('Upload Data', self)
        self._start_button.setFont(Qt.QFont('Roboto', 18))
        self._start_button.clicked.connect(self._push_data)
        grid.addWidget(self._start_button, 0, 1, 1, 1)
        # Table
        self.table = FinanceTableView()
        hbox = Qt.QHBoxLayout()
        hbox.addWidget(self.table)
        grid.addLayout(hbox, 1, 0, 1, 2)
        grid.setRowStretch(1, 1)
        # Grid
        self.setLayout(grid)


    def _load_data(self, links: list[str]):
        df_temp = parsing.csv_to_pandas(links[0])
        if parsing.pandas_in_known_files(df_temp):
            self._set_table_model(df_temp)
        else:
            self._add_file_type(df_temp)

    def _push_data(self):
        def run_command():
            BqApi().push_pd_to_bq(df=df, tabel=user.table_transactions, project=user.bq_project)
            Message(msg=f'Command inserted {df.shape[0]} new rows\n to {user.bq_project}.{user.table_transactions}', type='info', buttons='y').exec_()

        df = self.table.model.get_df()
        user = ProfileApi().get_user_class(target_name='dev')
        latest_date = BqApi().get_latest_date(tabel=user.table_transactions, project=user.bq_project)
        min_date = pd.to_datetime(df['date'].min(), format='%Y-%m-%d')
        if latest_date < min_date:
            run_command()
        else:
            dialog = Message(msg=f'Warning\nThere already exists data before {min_date:%Y-%m-%d}!\nProceed anyway?', type='warning', buttons='yn')
            if dialog.exec_() == QtWidgets.QMessageBox.Ok:
                print('accepted')
                run_command()


    def _set_table_model(self, df_temp: pd.DataFrame):
        df = parsing.process_pandas(df_temp)
        self.table.set_model(df)


    def _add_file_type(self, df_temp: pd.DataFrame):
        items = df_temp.columns.values.tolist()
        file_dialog = FileParsingDialog(items, parent=self)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                user_selections = file_dialog.selected_items()
                if user_selections['date_column'] == user_selections['receiver_column'] or user_selections['receiver_column'] == user_selections['amount_column']:
                    msg = Message(msg='Warning!\nFile columns must be uniquely identifiable', type='warning', buttons='y')
                    msg.exec_()
                else:
                    parsing.add_pandas_to_known_files(df_temp, 
                                                        name=user_selections['name'],
                                                        date_column=user_selections['date_column'],
                                                        date_format=user_selections['date_format'],
                                                        receiver_column=user_selections['receiver_column'],
                                                        amount_column=user_selections['amount_column'])
                    self._set_table_model(df_temp)
        else:
            msg = Message(msg='Warning!\nFile was not added', type='warning', buttons='y')
            msg.exec_()


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
            self._load_data(links)
        else:
            event.ignore()

      