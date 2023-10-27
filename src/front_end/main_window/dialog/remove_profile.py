from PyQt5 import QtCore
from PyQt5 import QtWidgets


class RemoveProfileDialog(QtWidgets.QDialog):
    def __init__(self, items, parent):
        super(RemoveProfileDialog, self).__init__(parent=parent)

        """ 
                print(parent.rect().bottomLeft())
                print(parent.rect().center()) """

        self.setWindowTitle('Remove Profile')
        self.resize(100, 100)

        grid = QtWidgets.QGridLayout() 
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(2, 1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel('Please provide required information.'))
        grid.addLayout(hbox, 0, 0, 1, 2)

        grid.addWidget(QtWidgets.QLabel('Name'), 1, 0, 1, 1)
        self._name = QtWidgets.QComboBox(self)
        self._name.addItems(items) 
        grid.addWidget(self._name, 1, 1, 1, 1)

        hbox = QtWidgets.QHBoxLayout()
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        hbox.addWidget(buttonBox)
        grid.addLayout(hbox, 3, 0, 1, 2)

        self.setLayout(grid)


    def selected_items(self):
        return self._name.currentText()