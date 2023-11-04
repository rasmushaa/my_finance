

from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
import pandas as pd


class PandasModel(QtCore.QAbstractTableModel):
	def __init__(self, df=pd.DataFrame(), parent=None):
		super().__init__(parent)
		self._df = df

	def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
		if role != QtCore.Qt.ItemDataRole.DisplayRole:
			return QtCore.QVariant()
		if orientation == QtCore.Qt.Orientation.Horizontal:
			try:
				return self._df.columns.tolist()[section]
			except IndexError:
				return QtCore.QVariant()
		elif orientation == QtCore.Qt.Orientation.Vertical:
			try:
				return self._df.index.tolist()[section]
			except IndexError:
				return QtCore.QVariant()

	def rowCount(self, parent=QtCore.QModelIndex()):
		return self._df.shape[0]

	def columnCount(self, parent=QtCore.QModelIndex()):
		return self._df.shape[1]
	
	def update(self, value, row):
		self.layoutAboutToBeChanged.emit()
		self._df.iloc[row, self.columnCount()-1] = value
		self.layoutChanged.emit()

	def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
		if role != QtCore.Qt.ItemDataRole.DisplayRole:
			return QtCore.QVariant()
		if not index.isValid():
			return QtCore.QVariant()
		return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))
	
	def get_value_at(self, rows: int, cols: int):
		return self._df.iloc[[rows], [cols]]
	
	def get_df(self):
		return self._df
	
	def get_df_col(self, col: int):
		return self._df.iloc[:, col]