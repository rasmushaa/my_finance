

from PyQt5              import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets    import QWidget, QMenu, QAction, QProgressBar, QLabel, QFileDialog, QTabWidget, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox, QGroupBox, QGridLayout, QTableView, QAbstractItemView
from PyQt5.QtCore       import Qt, QAbstractTableModel, QVariant, QModelIndex
from PyQt5.Qt import QDial, QSlider, QHBoxLayout, QPushButton, QFont, QMessageBox, QObject, QInputDialog

import pandas as pd
from src.back_end.utils import file_parsing


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
      

class TabTransaction(QWidget):
    def __init__(self, parent:object):
        super().__init__()
        self._parent = parent
        self._init_window()
        self.setAcceptDrops(True)

    
    def _init_window(self):
        grid = QGridLayout() 
        self.table = QTableView()
        vbox = QVBoxLayout()
        vbox.addWidget(self.table)
        grid.addLayout(vbox, 0, 0)
        self.setLayout(grid)


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

            print("GOT ADDRESS:\n",links)
            self.df = file_parsing.csv_to_pandas(links[0])
            if not file_parsing.pandas_in_known_files(self.df):
                  file_parsing.add_pandas_to_known_files(self.df, 1,2,3, 'testi')
				
            self.model = PandasModel(self.df)
            self.table.setModel(self.model)
            self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        else:
            event.ignore()


      