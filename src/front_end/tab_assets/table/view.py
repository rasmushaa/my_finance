

from PyQt5 import QtWidgets
from .model import PandasModel
from src.back_end.categories.api import CategoriesApi


class AssetsTableView(QtWidgets.QTableView):
    def __init__(self, active_user: str, parent=None):
        super().__init__(parent)
        self.window = parent
        self._set_model(user_name=active_user)
        self.verticalHeader().setSectionsMovable(True)
        self.verticalHeader().setDragEnabled(True)
        self.verticalHeader().sectionMoved.connect(self._update_indexing)


    def _set_model(self, user_name):
        df = CategoriesApi().get_assets_df(user_name=user_name)
        self._model = PandasModel(df)
        self.setModel(self._model)
        
        header = self.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    def get_df(self):
        return self._model.get_df()
    
    def _update_indexing(self):
        visual_indexes = [self.verticalHeader().visualIndex(row) for row in range(self._model.rowCount())]
        self._model.update_index(index=visual_indexes)
        df = self._model.get_df()
        df_dict = df.to_dict()
        order_dict = dict((v,k) for k,v in df_dict['category'].items()) # Swap key values
        CategoriesApi().update_assets_list_order(order_dict)