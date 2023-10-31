

from PyQt5 import QtCore
from PyQt5 import QtWidgets


class BqFilePushingDialog(QtWidgets.QDialog):
    def __init__(self, date, table, parent):
        super(BqFilePushingDialog, self).__init__(parent=parent)

        """ 
                print(parent.rect().bottomLeft())
                print(parent.rect().center()) """

        self.setWindowTitle('Warning')
        self.resize(100, 350)

        grid = QtWidgets.QGridLayout() 
        grid.setRowStretch(1, 1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel(f'There already exist data on {date}\nin {table}.\nProceed anyway?'))
        grid.addLayout(hbox, 0, 0, 2, 1)

        hbox = QtWidgets.QHBoxLayout()
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        hbox.addWidget(buttonBox)
        grid.addLayout(hbox, 2, 0, 2, 1)

        self.setLayout(grid)