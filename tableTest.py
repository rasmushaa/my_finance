import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QLineEdit, QTableView, QPushButton, QLabel, \
							QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex
from PyQt5.QtGui import QIcon

class PandasModel(QAbstractTableModel):
	def __init__(self, df=pd.DataFrame(), parent=None):
		super().__init__(parent)
		self._df = df

	def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
		if role != Qt.ItemDataRole.DisplayRole:
			return QVariant()
		if orientation == Qt.Orientation.Horizontal:
			try:
				return self._df.columns.tolist()[section]
			except IndexError:
				return QVariant()
		elif orientation == Qt.Orientation.Vertical:
			try:
				return self._df.index.tolist()[section]
			except IndexError:
				return QVariant()

	def rowCount(self, parent=QModelIndex()):
		return self._df.shape[0]

	def columnCount(self, parent=QModelIndex()):
		return self._df.shape[1]

	def data(self, index, role=Qt.ItemDataRole.DisplayRole):
		if role != Qt.ItemDataRole.DisplayRole:
			return QVariant()
		if not index.isValid():
			return QVariant()
		return QVariant(str(self._df.iloc[index.row(), index.column()]))



class MyApp(QWidget):
	def __init__(self):
		super().__init__()
		self.window_width, self.window_height = 1100, 500
		self.resize(self.window_width, self.window_height)
		self.setWindowTitle('CSV Data Viewer')
		self.setWindowIcon(QIcon('./icon/browser.png'))
		self.df = None
		self.setStyleSheet("""
			QWidget {
				font-size: 15px;
			}
			QComboBox {
				width: 160px;
			}
			QPushButton {
				width: 100px;
			}
		""")

		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		self.initUI()

	def retrieveDataset(self):
		# try:
		urlSource = self.dataSourceField.text()
		self.df = pd.read_csv(urlSource)
		self.df.fillna('')
		self.model = PandasModel(self.df)
		self.table.setModel(self.model)

		self.comboColumns.clear()
		self.comboColumns.addItems(self.df.columns)
		# except Exception as e:
		# 	self.statusLabel.setText(str(e))
		# 	return

	def searchItem(self, v):
		if self.df is None:
			return

		column_index = self.df.columns.get_loc(self.comboColumns.currentText())
		for row_index in range(self.model.rowCount()):
			if v in self.model.index(row_index, column_index).data():
				self.table.setRowHidden(row_index, False)
			else:
				self.table.setRowHidden(row_index, True)

	def initUI(self):
		sourceLayout = QHBoxLayout()
		self.layout.addLayout(sourceLayout)

		label = QLabel('&Data Source: ')
		self.dataSourceField = QLineEdit()
		label.setBuddy(self.dataSourceField)

		buttonRetrieve = QPushButton('&Retrieve', clicked=self.retrieveDataset)

		sourceLayout.addWidget(label)
		sourceLayout.addWidget(self.dataSourceField)
		sourceLayout.addWidget(buttonRetrieve)

		# search field
		searchLayout = QHBoxLayout()
		self.layout.addLayout(searchLayout)

		self.searchField = QLineEdit()
		self.searchField.textChanged.connect(self.searchItem)
		searchLayout.addWidget(self.searchField)

		self.comboColumns = QComboBox()
		searchLayout.addWidget(self.comboColumns)

		self.table = QTableView()
		self.table.setSortingEnabled(True)
		self.table.horizontalHeader().setSectionsMovable(True)
		self.layout.addWidget(self.table)

		self.statusLabel = QLabel()
		self.statusLabel.setText('')
		self.layout.addWidget(self.statusLabel)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet('''
		QWidget {
			font-size: 17px;
		}
	''')
	
	myApp = MyApp()
	myApp.show()

	try:
		sys.exit(app.exec())
	except SystemExit:
		print('Closing Window...')