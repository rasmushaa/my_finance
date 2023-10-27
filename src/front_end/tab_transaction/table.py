

from PyQt5 import QtWidgets
from PyQt5 import QtCore
import pandas as pd
from .model import PandasModel
from .category import CategoryCombo


class FinanceTableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.keyPressEvent = self._custom_navigation
        

    def set_model(self, df: pd.DataFrame):
        self.df = df
        self.model = PandasModel(self.df)
        self.setModel(self.model)

        for i in range(self.model.rowCount()):
            combo = CategoryCombo(row=i, parent=self)
            self.setIndexWidget(self.model.index(i, self.model.columnCount()-1), combo)

        header = self.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)


    def update_model(self, value: str, row: int):
        self.model.update(value, row)
        print(self.model.get_df())


    def get_category_at(self, row: int):
        return self.model.get_value_at(row=row, col=self.model.columnCount()-1)
    

    def set_focus_off_category(self):
        self.setCurrentIndex(self.model.index(self.currentIndex().row(), 0))
        self.setFocus()


    def set_focus_on_category(self):
        def get_index_widget ():
            return self.indexWidget(self.model.index(self.currentIndex().row(), self.model.columnCount()-1))
        get_index_widget().update_category_list(self.model.get_df_col(self.model.columnCount()-1).values)
        get_index_widget().setFocus()


    def _custom_navigation(self, event):
        if event.key() == QtCore.Qt.Key_Right:
            self.set_focus_on_category()
        return QtWidgets.QTableWidget.keyPressEvent(self, event) # Passthrough all default key events