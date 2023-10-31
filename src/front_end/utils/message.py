

from PyQt5 import QtWidgets


class Message(QtWidgets.QMessageBox):
    def __init__(self, msg: str, type: str = 'info', buttons: 'str' = 'yn', title: str = ''):
        super().__init__()
        self.setText(msg) 
        self.setWindowTitle(title)

        if type == 'info':
            self.setIcon(QtWidgets.QMessageBox.Information) 
        elif type == 'warning':
            self.setIcon(QtWidgets.QMessageBox.Warning) 
        elif type == 'question':
            self.setIcon(QtWidgets.QMessageBox.Question) 
        elif type == 'critical':
            self.setIcon(QtWidgets.QMessageBox.Critical) 

        if 'y' in buttons and 'n' in buttons:
            self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel) 
        elif 'y' in buttons and 'n' not in buttons:
            self.setStandardButtons(QtWidgets.QMessageBox.Ok) 
        elif 'n' in buttons and 'y' not in buttons:
            self.setStandardButtons(QtWidgets.QMessageBox.Cancel) 