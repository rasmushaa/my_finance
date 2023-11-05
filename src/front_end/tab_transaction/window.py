

from PyQt5 import QtWidgets
from PyQt5 import Qt
from PyQt5 import QtCore
import pandas as pd
from .dialog import FileParsingDialog
from .table import FinanceTableView
from src.front_end.utils import Message
from src.back_end import parsing
from src.back_end.bigquery import BqApi
from src.back_end.profiles import ProfileApi
from src.back_end.ml import MlApi


class TabTransaction(QtWidgets.QWidget):
    def __init__(self, parent:object):
        super().__init__()
        self.gui = parent
        self.ml_api = MlApi()
        self._init_window()
        self.setAcceptDrops(True)

    
    def _init_window(self):
        grid = QtWidgets.QGridLayout() 
        # User
        vbox = Qt.QVBoxLayout()
        user_name = self.gui.get_active_user()
        user = ProfileApi().get_user_class(target_name=user_name)
        user_label = QtWidgets.QLabel(user_name)
        user_label.setFont(Qt.QFont('Roboto', 22))
        vbox .addWidget(user_label)
        transaction_path = user.table_transactions
        transaction_path = f"{transaction_path.split('.')[0]} - {transaction_path.split('.')[1]}"
        transaction_label = QtWidgets.QLabel(transaction_path)
        transaction_label.setFont(Qt.QFont('Roboto', 16))
        vbox .addWidget(transaction_label)
        grid.addLayout(vbox , 0, 0, 1, 1)
        grid.setColumnStretch(0, 3)
        # Empty col
        grid.setColumnStretch(1, 4)
        # Push button
        self._start_button = QtWidgets.QPushButton('Upload Data', self)
        self._start_button.setFont(Qt.QFont('Roboto', 22))
        self._start_button.clicked.connect(self._push_data)
        self._start_button.setFixedHeight(70)
        self._start_button.setFixedWidth(200)
        grid.addWidget(self._start_button, 0, 2, 1, 1)
        grid.setColumnStretch(2, 0)
        # Table
        self.table = FinanceTableView(parent=self)
        hbox = Qt.QHBoxLayout()
        hbox.addWidget(self.table)
        grid.addLayout(hbox, 1, 0, 1, 3)
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
        user = ProfileApi().get_user_class(target_name=self.gui.get_active_user())
        latest_date = BqApi().get_latest_date(tabel=user.table_transactions, project=user.bq_project)
        min_date = pd.to_datetime(df['date'].min(), format='%Y-%m-%d')
        if latest_date < min_date:
            run_command()
        else:
            dialog = Message(msg=f'Warning\nThere already exists data after {min_date:%Y-%m-%d}!\nProceed anyway?', type='warning', buttons='yn')
            if dialog.exec_() == QtWidgets.QMessageBox.Ok:
                run_command()


    def _set_table_model(self, df_temp: pd.DataFrame):
        df = parsing.process_pandas(df_temp)
        self.table.set_model(df)
        user = self.gui.get_active_user()
        try:
            self.ml_api.load_model(name=user)
        except FileNotFoundError:
            dialog = Message(msg=f'Warning\nML model could not be loaded\nfor user: "{user}"\nProceeding without...', type='warning', buttons='y')
            dialog.exec_()


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

      