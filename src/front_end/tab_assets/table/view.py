

from PyQt5 import QtWidgets
import pandas as pd
from .model import PandasModel
from src.back_end.categories.api import CategoriesApi


class AssetsTableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = parent
        self._set_model()
        self.verticalHeader().setSectionsMovable(True)
        self.verticalHeader().setDragEnabled(True)
        self.verticalHeader().sectionMoved.connect(self._update_indexing)


    def _set_model(self,):
        df = pd.DataFrame(columns=['Category', 'Explanation', 'Value'])
        df['Category'] = CategoriesApi().get_assets_list()
        df['Explanation'] = CategoriesApi().get_assets_list_explanations()
        self._model = PandasModel(df)
        self.setModel(self._model)
        
        header = self.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def get_df(self):
        return self._model.get_df()
    
    def _update_indexing(self):
        visual_indexes = [self.verticalHeader().visualIndex(row) for row in range(self._model.rowCount())]
        self._model.update_index(index=visual_indexes)
        df = self._model.get_df()
        df_dict = df.to_dict()
        order_dict = dict((v,k) for k,v in df_dict['Category'].items()) # Swap key values
        CategoriesApi().update_assets_list_order(order_dict)