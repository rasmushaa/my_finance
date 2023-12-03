

from PyQt5 import QtWidgets
from PyQt5 import Qt
import pandas as pd
from .table import AssetsTableView
from src.front_end.utils import Message
from src.back_end.bigquery import BqApi
from src.back_end.profiles import ProfileApi


class TabAssets(QtWidgets.QWidget):
    def __init__(self, parent:object):
        super().__init__()
        self.gui = parent
        self._init_window()

    
    def _init_window(self):
        grid = QtWidgets.QGridLayout() 
        # User
        vbox = Qt.QVBoxLayout()
        user_name = self.gui.get_active_user()
        user = ProfileApi().get_user_class(target_name=user_name)
        user_label = QtWidgets.QLabel(user_name)
        user_label.setFont(Qt.QFont('Roboto', 22))
        vbox .addWidget(user_label)
        assets_path = user.table_assets
        assets_path = f"{assets_path.split('.')[0]}.{assets_path.split('.')[1]}"
        assets_label = QtWidgets.QLabel(assets_path)
        assets_label.setFont(Qt.QFont('Menlo', 14))
        vbox.addWidget(assets_label)
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
        self.table = AssetsTableView(active_user=self.gui.get_active_user(), parent=self)
        hbox = Qt.QHBoxLayout()
        hbox.addWidget(self.table)
        grid.addLayout(hbox, 1, 0, 1, 3)
        grid.setRowStretch(1, 1)
        # Grid
        self.setLayout(grid)


    def _push_data(self):
        def run_command():
            BqApi().push_pd_to_bq(df=df, tabel=user.table_assets, project=user.bq_project)
            Message(msg=f'Command inserted {df.shape[0]} new rows\n to {user.bq_project}.{user.table_assets}', type='info', buttons='y').exec_()

        df = self.table.get_df()
        user = ProfileApi().get_user_class(target_name=self.gui.get_active_user())
        latest_date = BqApi().get_latest_date(tabel=user.table_assets, project=user.bq_project)
        min_date = pd.to_datetime(df['date'].min(), format='%Y-%m-%d')
        if latest_date < min_date:
            run_command()
        else:
            dialog = Message(msg=f'Warning\nThere already exists data after {min_date:%Y-%m-%d}\nProceed anyway?', type='warning', buttons='yn')
            if dialog.exec_() == QtWidgets.QMessageBox.Ok:
                run_command()