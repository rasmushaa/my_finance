

from PyQt5 import QtCore
from PyQt5 import QtWidgets


class FileParsingDialog(QtWidgets.QDialog):
    def __init__(self, items, parent):
        super(FileParsingDialog, self).__init__(parent=parent)

        """ 
                print(parent.rect().bottomLeft())
                print(parent.rect().center()) """

        self.setWindowTitle('Unknown file')
        self.resize(100, 350)

        grid = QtWidgets.QGridLayout() 

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel('Please provide reuired information.'))
        grid.addLayout(hbox, 0, 0, 2, 1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel('Name'))
        self._input_name = QtWidgets.QLineEdit()
        hbox.addWidget(self._input_name)
        grid.addLayout(hbox, 1, 0, 2, 1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel('Date'))
        self._input_date_column = QtWidgets.QComboBox(self)
        self._input_date_column.addItems(items) 
        hbox.addWidget(self._input_date_column)
        grid.addLayout(hbox, 2, 0, 2, 1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel('Format'))
        self._input_date_format = QtWidgets.QComboBox(self)
        allowed_formats = ['%Y-%m-%d', '%d.%m.%Y', '%m/%d/%Y']
        self._input_date_format.addItems(allowed_formats) 
        hbox.addWidget(self._input_date_format)
        grid.addLayout(hbox, 3, 0, 2, 1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel('Receiver'))
        self._input_receiver_column = QtWidgets.QComboBox(self)
        self._input_receiver_column.addItems(items) 
        hbox.addWidget(self._input_receiver_column)
        grid.addLayout(hbox, 4, 0, 2, 1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel('Amount'))
        self._input_amount_column = QtWidgets.QComboBox(self)
        self._input_amount_column.addItems(items) 
        hbox.addWidget(self._input_amount_column)
        grid.addLayout(hbox, 5, 0, 2, 1)

        hbox = QtWidgets.QHBoxLayout()
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        hbox.addWidget(buttonBox)
        grid.addLayout(hbox, 6, 0, 2, 1)

        self.setLayout(grid)


    def selected_items(self):
        values = {'name': self._input_name.text(), 
                  'date_column': self._input_date_column.currentText(),
                  'date_format': self._input_date_format.currentText(),
                  'receiver_column': self._input_receiver_column.currentText(),
                  'amount_column': self._input_amount_column.currentText()}
        return values