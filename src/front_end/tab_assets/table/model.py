

from PyQt5 import QtCore
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

	def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
		if role != QtCore.Qt.ItemDataRole.DisplayRole:
			return QtCore.QVariant()
		if not index.isValid():
			return QtCore.QVariant()
		return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))
	
	def get_df(self):
		return self._df.copy()
	
	def setData(self, index, value, role=QtCore.Qt.EditRole):
		if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
			if index.column() == 0:
				try:
					value = pd.to_datetime(value, format='%Y-%m-%d').date()
				except ValueError:
					raise ValueError('Only "%Y-%m-%d" format is supported')
				self._df.iloc[:, [index.column()]] = value
			if index.column() == 3:
				try:
					value = float(value)
				except ValueError:
					raise ValueError('Only numeric values are allowed')
				self._df.iloc[[index.row()], [index.column()]] = value
			self.dataChanged.emit(index, index)
		return True
	
	def update_index(self, index):
		self._df.index = index

	def flags(self, index):
		if (index.column() == 0 or index.column() == 3):
			return super().flags(index) | QtCore.Qt.ItemIsEditable
		return QtCore.Qt.ItemIsEnabled #| QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled 
