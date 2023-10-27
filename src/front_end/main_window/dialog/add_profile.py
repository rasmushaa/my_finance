from PyQt5 import QtCore
from PyQt5 import QtWidgets


class AddProfileDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(AddProfileDialog, self).__init__(parent=parent)

        """ 
                print(parent.rect().bottomLeft())
                print(parent.rect().center()) """

        self.setWindowTitle('Add Profile')
        self.resize(500, 200)

        grid = QtWidgets.QGridLayout() 
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(6, 1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel('Please provide required information.'))
        grid.addLayout(hbox, 0, 0, 1, 2)

        grid.addWidget(QtWidgets.QLabel('Name'), 1, 0, 1, 1)
        self._name = QtWidgets.QLineEdit()
        grid.addWidget(self._name, 1, 1, 1, 1)

        grid.addWidget(QtWidgets.QLabel('BQ Account'), 2, 0, 1, 1)
        self._account = QtWidgets.QLineEdit()
        grid.addWidget(self._account, 2, 1, 1, 1)

        grid.addWidget(QtWidgets.QLabel('BQ Project ID'), 3, 0, 1, 1)
        self._project = QtWidgets.QLineEdit()
        grid.addWidget(self._project, 3, 1, 1, 1)

        grid.addWidget(QtWidgets.QLabel('Transaction Table Path'), 4, 0, 1, 1)
        self._transaction_table = QtWidgets.QLineEdit()
        grid.addWidget(self._transaction_table, 4, 1, 1, 1)

        grid.addWidget(QtWidgets.QLabel('Assets Table Path'), 5, 0, 1, 1)
        self._assets_table = QtWidgets.QLineEdit()
        grid.addWidget(self._assets_table, 5, 1, 1, 1)

        hbox = QtWidgets.QHBoxLayout()
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        hbox.addWidget(buttonBox)
        grid.addLayout(hbox, 7, 0, 1, 2)

        self.setLayout(grid)


    def selected_items(self):
        values = {'name': self._name.text(), 
                  'bq_account': self._account.text(),
                  'bq_project': self._project.text(),
                  'table_transactions': self._transaction_table.text(),
                  'table_assets': self._assets_table.text()
                  }
        return values