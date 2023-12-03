

from PyQt5 import QtWidgets
from PyQt5 import QtCore


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
    def __init__(self, row: int, items: list, parent):
        super().__init__(parent)
        self._parent = parent
        self._row = row
        self._default_items = items
        self.addItems([''])
        self.currentTextChanged.connect(self.update_value)
        self.setView(MyView(parent=self))
        self.keyPressEvent = self._custom_navigation
        self._inital_value = self.currentText()


    def update_value(self):
        self._parent.update_model(self.currentText(), row=self._row)


    def set_categories(self, category_list: list):
        self.clear()
        self.addItems(category_list)


    def _custom_navigation(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            if self._inital_value in {self.itemText(i) for i in range(self.count())}:
                self.setCurrentText(self._inital_value)
            else:
                self.addItems([''])
                self.setCurrentText(self._inital_value)
            self._parent.set_focus_off_category()
        elif event.key() == QtCore.Qt.Key_Return:
            self._inital_value = self.currentText()
            self._parent.update_model(self.currentText(), row=self._row)
            self._parent.set_focus_off_category()
        elif event.key() == QtCore.Qt.Key_Right:
            self.set_categories(self._default_items)
            self.showPopup()
        return QtWidgets.QComboBox.keyPressEvent(self, event) # Passthrough all default key events