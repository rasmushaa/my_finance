

from PyQt5              import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets    import QWidget, QMenu, QAction, QProgressBar, QLabel, QFileDialog, QTabWidget, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox, QGroupBox, QGridLayout
from PyQt5.QtCore       import Qt, QThread, pyqtSignal
from PyQt5.Qt import QDial, QSlider, QHBoxLayout, QPushButton, QFont, QMessageBox, QObject, QInputDialog
from src.back_end.profiles import ProfileApi
from src.front_end.tab_transaction import TabTransaction
from .dialog.add_profile import AddProfileDialog
from .dialog.remove_profile import RemoveProfileDialog


class GUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_menu_bar()
         
        
    def _init_window(self):

        self.setGeometry(300, 100, 900, 600)
        self.setWindowTitle('GUI Template')  
         # Add tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(TabTransaction(self), 'Transactions')
        self.tabs.addTab(QWidget(), " 3 ")
        self.setCentralWidget(self.tabs)
        self.show()
        
        
    def _init_menu_bar(self):
        menu_main = self.menuBar()
        # Profiles
        menu_profiles = menu_main.addMenu("&Profiles")
        action = QAction('&Add profile', self)
        action.triggered.connect(self._add_profile) 
        menu_profiles.addAction(action)
        action = QAction('&Remove profile', self)
        action.triggered.connect(self._remove_profile) 
        menu_profiles.addAction(action)
        

    def _add_profile(self):
        file_dialog = AddProfileDialog(parent=self)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                inputs = file_dialog.selected_items()
                ProfileApi().add_profile(name=inputs['name'],
                                             bq_account=inputs['bq_account'],
                                             bq_project=inputs['bq_project'],
                                             table_transactions=inputs['table_transactions'],
                                             table_assets=inputs['table_assets'])

    def _remove_profile(self):
        values = ProfileApi().get_profile_names()
        file_dialog = RemoveProfileDialog(items=values, parent=self)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                name = file_dialog.selected_items()
                ProfileApi().remove_profile(target_name=name)