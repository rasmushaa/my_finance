

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from back_end.categories import CategoriesApi 

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
        #self.currentIndexChanged.connect(self.update_value)
        self.setView(MyView(parent=self))
        self.keyPressEvent = self._custom_navigation
        self._inital_value = self.currentText()


    def update_value(self):
        self._parent.update_model(self.currentText(), row=self._row)


    def set_prediction_categories(self, category_list: list):
        self.clear()
        self.addItems(category_list)

    def set_default_categories(self):
        self.clear()
        self.addItems(CategoriesApi().get_transaction_list())
    

    def _custom_navigation(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            if self._inital_value in {self.itemText(i) for i in range(self.count())}:
                self.setCurrentText(self._inital_value)
            else:
                self.set_default_categories()
                self.setCurrentText(self._inital_value)
            self._parent.set_focus_off_category()
        elif event.key() == QtCore.Qt.Key_Return:
            self._inital_value = self.currentText()
            self._parent.update_model(self.currentText(), row=self._row)
            self._parent.set_focus_off_category()
        elif event.key() == QtCore.Qt.Key_Right:
            self.set_default_categories()
            self.showPopup()
        return QtWidgets.QComboBox.keyPressEvent(self, event) # Passthrough all default key events