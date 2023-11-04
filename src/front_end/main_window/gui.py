

from PyQt5              import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets    import QWidget, QMenu, QAction, QProgressBar, QLabel, QFileDialog, QTabWidget, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox, QGroupBox, QGridLayout
from PyQt5.QtCore       import Qt, QThread, pyqtSignal
from PyQt5.Qt import QDial, QSlider, QHBoxLayout, QPushButton, QFont, QMessageBox, QObject, QInputDialog
from .dialog.add_profile import AddProfileDialog
from .dialog.remove_profile import RemoveProfileDialog
from src.front_end.tab_transaction import TabTransaction
from src.back_end.profiles import ProfileApi
from src.back_end.ml import MlApi
from src.back_end.bigquery import BqApi


class GUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_menu_bar()
         
        
    def _init_window(self):
        self.setGeometry(300, 100, 900, 600)
        self.setWindowTitle('GUI Template')  
         # Add tabs
        self._add_tabs()

    def _add_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(TabTransaction(self), 'Transactions')
        self.tabs.addTab(QWidget(), " 3 ")
        self.setCentralWidget(self.tabs)
        self.update_active_user(ProfileApi().get_profile_names()[0])
        self.show()


    def update_active_user(self, user: str):
        self._active_user = user

    def get_active_user(self):
         return self._active_user    
        
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
        # Ml
        menu_ml = menu_main.addMenu("&Model")
        action = QAction('&Train', self)
        action.triggered.connect(self._train_model) 
        menu_ml.addAction(action)
        

    def _add_profile(self):
        file_dialog = AddProfileDialog(parent=self)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                inputs = file_dialog.selected_items()
                ProfileApi().add_profile(name=inputs['name'],
                                             bq_project=inputs['bq_project'],
                                             table_transactions=inputs['table_transactions'],
                                             table_assets=inputs['table_assets'])
                self._add_tabs()

    def _remove_profile(self):
        values = ProfileApi().get_profile_names()
        file_dialog = RemoveProfileDialog(items=values, parent=self)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                name = file_dialog.selected_items()
                ProfileApi().remove_profile(target_name=name)

    def _train_model(self):
         user = ProfileApi().get_user_class(target_name=self.get_active_user())
         sql = f"SELECT receiver, category FROM {user.table_transactions}"
         df = BqApi().pull_pd_from_bq(sql, project=user.bq_project)
         MlApi().train_new_model(data=df, target_col='category', name=self._active_user)