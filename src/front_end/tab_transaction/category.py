

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from src.back_end import categories

class MyView(QtWidgets.QListView):
    def __init__(self, parent):
            super().__init__(parent)
            self._parent = parent
            self.keyPressEvent = self._custom_navigation

    def _custom_navigation(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self._parent.hidePopup()
        if event.key() == QtCore.Qt.Key_Return:
            self._parent._inital_value = self._parent.currentText()
            self._parent._parent.set_focus_off_category()
            self._parent.hidePopup()
        return QtWidgets.QListView.keyPressEvent(self, event) # Passthrough all default key events
    

class CategoryCombo(QtWidgets.QComboBox):
    def __init__(self, row: int, parent):
        super().__init__(parent)
        self._parent = parent
        self._row = row
        self.addItems([''])
        self.currentIndexChanged.connect(self.update_value)
        self.setView(MyView(parent=self))
        self.keyPressEvent = self._custom_navigation
        self._inital_value = self.currentText()


    def update_value(self):
        self._parent.update_model(self.currentText(), row=self._row)


    def update_category_list(self, current_categories: list):
        self.clear()
        self.addItems(categories.get_transaction_list())
    

    def _custom_navigation(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.setCurrentText(self._inital_value)
            self._parent.set_focus_off_category()
        elif event.key() == QtCore.Qt.Key_Return:
            self._inital_value = self.currentText()
            self._parent.set_focus_off_category()
        elif event.key() == QtCore.Qt.Key_Right:
            self.showPopup()
        return QtWidgets.QComboBox.keyPressEvent(self, event) # Passthrough all default key events