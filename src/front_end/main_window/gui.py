

import json
import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTabWidget, QAction
from .dialog import AddProfileDialog, AddAssetDialog, AddTransactionDialog, SelectionDialog
from src.front_end.tab_transaction import TabTransaction
from src.front_end.tab_assets import TabAssets
from src.front_end.utils import Message
from src.back_end.profiles import ProfileApi
from src.back_end.parsing import FileParsingApi
from src.back_end.categories import CategoriesApi
from src.back_end.ml import MlApi
from src.back_end.bigquery import BqApi

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    BASE_PATH = sys._MEIPASS
except Exception:
    BASE_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '..'))
FILE_NAME = 'gui_state.json'


class GUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._load_state()
        self._init_window()
        self._init_menu_bar()
        self._init_tabs()

    def closeEvent(self, event):
        self._update_state() 
        with open(f'{BASE_PATH}/{FILE_NAME}', 'w') as f:
            json.dump(self._state, f, ensure_ascii=False, indent=4)
         
    def _load_state(self):
        try:
            with open(f'{BASE_PATH}/{FILE_NAME}', 'r') as f:
                self._state = json.load(f)
        except FileNotFoundError:
            self._update_state(use_default=True)   

    def _update_state(self, use_default=False):
        self._state = {}
        if use_default:
            self._state.update({'geometry': self.geometry().getRect()})
            self._state.update({'active_user': 'not_set'})   
        else:
            self._state.update({'geometry': self.geometry().getRect()})
            self._state.update({'active_user': self.get_active_user()})

    def _init_window(self):
        (ax, ay, aw, ah) = self._state['geometry']
        self.setGeometry(ax, ay, aw, ah)
        self.setWindowTitle(f'My Finance')  
        self.show()
        self._set_initial_user()

    def _set_initial_user(self):
        def verify_user_list():
            user = ProfileApi().get_profile_names()[0] # If users list is empy, API returns [None]
            while user is None:
                dialog = Message(msg=f'In order to use the application, at least one profile must be created', type='info', buttons='yn')
                if dialog.exec_() == QtWidgets.QMessageBox.Cancel:
                     sys.exit()
                self._add_profile()
                user = ProfileApi().get_profile_names()[0]
        verify_user_list()
        last_active_user = self._state['active_user']
        users = ProfileApi().get_profile_names()
        if last_active_user in users:
            self._active_user = last_active_user
        else:
             self._active_user = users[0]

    def _init_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(TabTransaction(self), 'Transactions')
        self.tabs.addTab(TabAssets(self), "Assets")
        self.setCentralWidget(self.tabs)

    def get_active_user(self):
        return self._active_user    
        
    def _init_menu_bar(self):
        self.menuBar().clear()
        menu_main = self.menuBar()
        # Profiles
        menu_profiles = menu_main.addMenu("&Profiles")
        # Profiles sub selection
        menu_profiles_select = menu_profiles.addMenu("&Select profile")
        users = ProfileApi().get_profile_names()
        for index, user in enumerate(users):
            name = "%s - %s" % (index, user)
            action = QAction(f'&{name}', self)
            action.setData(user)
            action.triggered.connect(self._select_profile)
            menu_profiles_select.addAction(action)
        action = QAction('&Add profile', self)
        action.triggered.connect(self._add_profile) 
        menu_profiles.addAction(action)
        action = QAction('&Remove profile', self)
        action.triggered.connect(self._remove_profile) 
        menu_profiles.addAction(action)
        # Banking
        menu_bank = menu_main.addMenu("&Banking")
        menu_bank_labels = menu_bank.addMenu("&Labels")
        action = QAction('&Add transaction', self)
        action.triggered.connect(self._add_transaction) 
        menu_bank_labels.addAction(action)
        action = QAction('&Remove transaction', self)
        action.triggered.connect(self._remove_transaction) 
        menu_bank_labels.addAction(action)
        action = QAction('&Add asset', self)
        action.triggered.connect(self._add_asset) 
        menu_bank_labels.addAction(action)
        action = QAction('&Remove asset', self)
        action.triggered.connect(self._remove_asset) 
        menu_bank_labels.addAction(action)
        action = QAction('&Remove file', self)
        action.triggered.connect(self._remove_banking_file) 
        menu_bank.addAction(action)
        # Ml
        menu_ml = menu_main.addMenu("&Model")
        action = QAction('&Train for user', self)
        action.triggered.connect(self._train_model) 
        menu_ml.addAction(action)

    
    def _select_profile(self):
        action = self.sender()
        self._active_user = action.data()
        self._init_tabs()

    def _add_profile(self):
        file_dialog = AddProfileDialog(parent=self)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                inputs = file_dialog.selected_items()
                ProfileApi().add_profile(name=inputs['name'],
                                             bq_project=inputs['bq_project'],
                                             table_transactions=inputs['table_transactions'],
                                             table_assets=inputs['table_assets'])
                self._init_menu_bar()

    def _remove_profile(self):
        values = ProfileApi().get_profile_names()
        file_dialog = SelectionDialog(items=values, parent=self)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                name = file_dialog.selected_items()
                ProfileApi().remove_profile(target_name=name)
                self._set_initial_user()
                self._init_menu_bar()
                self._init_tabs()

    def _add_transaction(self):
        file_dialog = AddTransactionDialog(parent=self)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                inputs = file_dialog.selected_items()
                CategoriesApi().add_transaction(name=inputs['name'], user_name=self.get_active_user())
                self._init_tabs()

    def _remove_transaction(self):
        values = CategoriesApi().get_transaction_list(user_name=self.get_active_user())
        file_dialog = SelectionDialog(items=values, parent=self)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                name = file_dialog.selected_items()
                CategoriesApi().remove_transaction(name=name, user_name=self.get_active_user())
                self._init_tabs()

    def _add_asset(self):
        file_dialog = AddAssetDialog(parent=self)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                inputs = file_dialog.selected_items()
                CategoriesApi().add_asset(name=inputs['name'], 
                                          explanation=inputs['explanation'], 
                                          user_name=self.get_active_user())
                self._init_tabs()

    def _remove_asset(self):
        values = CategoriesApi().get_assets_list(user_name=self.get_active_user())
        file_dialog = SelectionDialog(items=values, parent=self)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                name = file_dialog.selected_items()
                CategoriesApi().remove_asset(name=name, user_name=self.get_active_user())
                self._init_tabs()

    def _remove_banking_file(self):
        values = FileParsingApi().get_known_files()
        file_dialog = SelectionDialog(items=values, parent=self)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                name = file_dialog.selected_items()
                FileParsingApi().remove_known_file(filename=name)

    def _train_model(self):
        user = ProfileApi().get_user_class(target_name=self.get_active_user())
        sql = f"SELECT receiver, category FROM {user.table_transactions} WHERE category != ''"
        df = BqApi().pull_pd_from_bq(sql, project=user.bq_project)
        if len(df) > 0:
            MlApi().train_new_model(data=df, target_col='category', name=self.get_active_user())
            Message(msg=f'A new ML model trained for user "{self.get_active_user()}"\nusing {df.shape[0]} rows from {user.table_transactions}', type='info', buttons='y').exec_()
            probs = MlApi().get_propabilities(name=self.get_active_user())
            CategoriesApi().update_transaction_list_order(probs, user_name=self.get_active_user())
            self._init_tabs()
        else:
            Message(msg=f'There is not enough data in {user.table_transactions}\nMinimum number of rows is 1', type='warning', buttons='y').exec_()