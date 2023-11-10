

from PyQt5 import QtWidgets
from PyQt5 import Qt
from PyQt5 import QtCore
import pandas as pd
from .table import AssetsTableView
from src.front_end.utils import Message
from src.back_end.parsing import FileParsingApi
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
        assets_path = f"{assets_path.split('.')[0]} - {assets_path.split('.')[1]}"
        assets_label = QtWidgets.QLabel(assets_path)
        assets_label.setFont(Qt.QFont('Roboto', 16))
        vbox .addWidget(assets_label)
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
        self.table = AssetsTableView(parent=self)
        hbox = Qt.QHBoxLayout()
        hbox.addWidget(self.table)
        grid.addLayout(hbox, 1, 0, 1, 3)
        grid.setRowStretch(1, 1)
        # Grid
        self.setLayout(grid)


    def _push_data(self):
        print(self.table.get_df())