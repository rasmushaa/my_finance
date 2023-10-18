

from PyQt5              import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets    import QWidget, QMenu, QAction, QProgressBar, QLabel, QFileDialog, QTabWidget, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox, QGroupBox, QGridLayout
from PyQt5.QtCore       import Qt, QThread, pyqtSignal
from PyQt5.Qt import QDial, QSlider, QHBoxLayout, QPushButton, QFont, QMessageBox, QObject, QInputDialog
from src.back_end.application import App
from src.front_end.tab_transaction import TabTransaction
from src.front_end.tab_raysar import TabRaySar

class GUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.app = App()
        self._init_window()
        self._init_tool_bar()
        
    
    ###################### GUI INITS #########################    
        
    def _init_window(self):

        self.setGeometry(300, 100, 900, 600)
        self.setWindowTitle('GUI Template')
        
         # Add tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(TabTransaction(self), 'Transactions')
        self.tabs.addTab(TabRaySar(self), " RaySAR ")
        self.tabs.addTab(QWidget(), " 3 ")
        
        self.setCentralWidget(self.tabs)
        self.show()
        
        
        
    def _init_tool_bar(self):
        toolbar = self.addToolBar('toolbar')

        action = QAction('Load file', self)
        action.triggered.connect(self.new_file) 
        toolbar.addAction(action)

        action = QAction('Select save path', self)
        action.triggered.connect(self.save_file)
        toolbar.addAction(action)

        action = QAction('Set save name', self)
        action.triggered.connect(self.change_save_name)
        toolbar.addAction(action)
        
     
        
        
    ###################### ACTION HANDELS #########################    
    
    def update_pbar(self, value):
        self.pbar.setValue(value)
    
    def new_file(self):
        
        dir_path = QFileDialog.getOpenFileName(self,"Choose file to open")
        if self.app.load_model_file(dir_path[0]):
            self.message_box("File couldn't be loaded!")
        else:
            self.model_file_label.setText(dir_path[0])
        
    def save_file(self):
        dir_path = QFileDialog.getExistingDirectory(self,"Choose save file location")
        print(dir_path)
        self.save_file_label.setText(dir_path)
    
    
    def change_save_name(self):
        items = ("1 file_Az_Po",
                 "2 file-Az-Po",
                 "3 file Az Po",
                 "4 file,Az,Po",
                 "5 file  Az    Po",
                 "6 file_Running index")
            
        item, ok = QInputDialog.getItem(self, "Select save file numbering type", 
            "List of types:", items, 0, False)
        
                
        if ok and item:
            print(item)
         
        
                
    def change_azimuth1(self, value):   
        if self.app.set_start_az(value):
            self.message_box("Start value can't be larger than last value!")
        
    def change_azimuth2(self, value):
        if self.app.set_end_az(value):
            self.message_box("End value can't be smaller than starting value!")
        
    def change_azimuth12(self, value):
        if self.app.set_delta_az(value):
            self.message_box("Increment value has to be positive!")

    def change_polar1(self, value):
        if self.app.set_start_po(value):
            self.message_box("Start value can't be larger than last value!")
        
    def change_polar2(self, value):
        if self.app.set_end_po(value):
            self.message_box("End value can't be smaller than starting value!")
        
    def change_polar12(self, value):
        if self.app.set_delta_po(value):
            self.message_box("Increment value has to be positive!")
        
        
    def start_progres(self):
        '''
        Starts working with the computing task
        in a new thread. Connected to start button states.
        '''
        if self.start_button.isChecked():
            self.start_button.setStyleSheet("background-color : red")
            self.start_button.setText("STOP")
            
            # Creates worker in a new thread for computing
            self.thread = QThread()
            self.worker = Worker(self)
            self.worker.moveToThread(self.thread)
            
            # Clean exit of thread and worker
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            
            # Connects resets
            self.worker.update_signal.connect(self.update_pbar)
            self.thread.finished.connect(
                lambda: self.start_button.setText("START")
            )
            self.thread.finished.connect(
                lambda: self.start_button.setStyleSheet("background-color : lightgreen")
            )
            self.thread.finished.connect(
                lambda: self.start_button.setChecked(False)
            )
            
            self.thread.start()
                  
        else:
            self.worker.stop_task()
            self.start_button.setStyleSheet("background-color : lightgreen")
            self.start_button.setText("START")
            self.message_box("Generating images was canceled...")

        
    ################### HELPER FUNCTIONS ######################
        
    def message_box(self, msg):     
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Critical) 
        msgbox.setText(msg)
        msgbox.exec_()
        


'''
Worker does long running tasks after it has
been mowed to a new thread.
Update signal can be passed to task and
be used to control progress bar.
'''
class Worker(QObject):
    
    # signals to monitor working thread
    finished = pyqtSignal()
    update_signal = pyqtSignal(int)
    
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        
    def stop_task(self):
        self.gui.app.set_running(False)


    def run(self):   
        self.gui.app.compute(self.update_signal)       
        self.finished.emit()



        