from PyQt5 import QtCore
from PyQt5 import QtWidgets


class AddAssetDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(AddAssetDialog, self).__init__(parent=parent)

        """ 
                print(parent.rect().bottomLeft())
                print(parent.rect().center()) """

        self.setWindowTitle('Add Profile')
        self.resize(500, 200)

        grid = QtWidgets.QGridLayout() 
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(3, 1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel('Please provide required information.'))
        grid.addLayout(hbox, 0, 0, 1, 2)

        grid.addWidget(QtWidgets.QLabel('Name'), 1, 0, 1, 1)
        self._name = QtWidgets.QLineEdit()
        grid.addWidget(self._name, 1, 1, 1, 1)

        grid.addWidget(QtWidgets.QLabel('Explanation'), 2, 0, 1, 1)
        self._explanation = QtWidgets.QLineEdit()
        grid.addWidget(self._explanation, 2, 1, 1, 1)

        hbox = QtWidgets.QHBoxLayout()
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        hbox.addWidget(buttonBox)
        grid.addLayout(hbox, 4, 0, 1, 2)

        self.setLayout(grid)


    def selected_items(self):
        values = {'name': self._name.text(), 
                  'explanation': self._explanation.text(),
                  }
        return values