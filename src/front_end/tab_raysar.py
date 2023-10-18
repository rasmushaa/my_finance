
from PyQt5              import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets    import QWidget, QMenu, QAction, QProgressBar, QLabel, QFileDialog, QTabWidget, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox, QGroupBox, QGridLayout
from PyQt5.QtCore       import Qt, QThread, pyqtSignal
from PyQt5.Qt import QDial, QSlider, QHBoxLayout, QPushButton, QFont, QMessageBox, QObject, QInputDialog

class TabRaySar(QWidget):
    def __init__(self, parent:object):
        super().__init__()
        self._parent = parent
        self._init_window()

    
    def _init_window(self):
        '''
        Adds controls and labels for tab1 
        and connects them to action handles
        '''
        # the main grid
        grid = QGridLayout() 
        #vertical group for settings
        group_box = QGroupBox("Coordinate settings")
        vbox = QVBoxLayout()
        
        '''
        first group
        '''
        # title of slider 1
        label = QLabel("Start azimuth")
        vbox.addWidget(label)
        # horizontal box for slider and label
        hbox = QHBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(360)
        slider.setValue(1)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(85)
        label = QLabel()
        label.setMinimumWidth(25)
        label.setNum(slider.value())
        slider.valueChanged.connect(label.setNum)
        #slider.valueChanged.connect(self.change_azimuth1)  
        #self.change_azimuth1(slider.value())
        # add slider and label to vertical layout
        hbox.addWidget(slider)
        hbox.addWidget(label)
        vbox.addLayout(hbox)
        
        # title of slider 2
        label = QLabel("End azimuth")
        vbox.addWidget(label)
        # horizontal box for slider and label
        hbox = QHBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(360)
        slider.setValue(360)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(85)
        label = QLabel()
        label.setMinimumWidth(25)
        label.setNum(slider.value())
        slider.valueChanged.connect(label.setNum)
        #slider.valueChanged.connect(self.change_azimuth2)  
        #self.change_azimuth2(slider.value())
        # add slider and label to vertical layout
        hbox.addWidget(slider)
        hbox.addWidget(label)
        vbox.addLayout(hbox)
        
        # horizontal box for dial 1 and label
        hbox = QHBoxLayout()
        vbox2 = QVBoxLayout()
        dial = QDial()
        dial.setMinimum(1)
        dial.setMaximum(20)
        dial.setValue(10)
        dial.setNotchesVisible(True)
        dial.setFixedSize(100, 100)
        label = QLabel("Increments [0.1°]")
        vbox2.addStretch(1)
        vbox2.addWidget(label)
        label = QLabel()
        vbox2.addWidget(label)
        vbox2.addStretch(1)
        label.setNum(dial.value())
        dial.valueChanged.connect(label.setNum)
        #dial.valueChanged.connect(self.change_azimuth12)
        #self.change_azimuth12(dial.value())
        
        hbox.addWidget(dial)
        hbox.addLayout(vbox2) 
        vbox.addLayout(hbox)
        
        '''
        Second group
        '''
        # title of slider 1
        label = QLabel("Start polar")
        vbox.addWidget(label)
        # horizontal box for slider and label
        hbox = QHBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(90)
        slider.setValue(23)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(22)
        label = QLabel()
        label.setMinimumWidth(25)
        label.setNum(slider.value())
        slider.valueChanged.connect(label.setNum)
        #slider.valueChanged.connect(self.change_polar1)  
        #self.change_polar1(slider.value())
        # add slider and label to vertical layout
        hbox.addWidget(slider)
        hbox.addWidget(label)
        vbox.addLayout(hbox)
        
        # title of slider 2
        label = QLabel("End polar")
        vbox.addWidget(label)
        # horizontal box for slider and label
        hbox = QHBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(90)
        slider.setValue(23)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(22)
        label = QLabel()
        label.setMinimumWidth(25)
        label.setNum(slider.value())
        slider.valueChanged.connect(label.setNum)
        #slider.valueChanged.connect(self.change_polar2)  
        #self.change_polar2(slider.value())
        # add slider and label to vertical layout
        hbox.addWidget(slider)
        hbox.addWidget(label)
        vbox.addLayout(hbox)
        
        # horizontal box for dial 1 and label
        hbox = QHBoxLayout()
        vbox2 = QVBoxLayout()
        dial = QDial()
        dial.setMinimum(1)
        dial.setMaximum(20)
        dial.setValue(10)
        dial.setNotchesVisible(True)
        dial.setFixedSize(100, 100)
        label = QLabel("Increments [0.1°]")
        vbox2.addStretch(1)
        vbox2.addWidget(label)
        label = QLabel()
        vbox2.addWidget(label)
        vbox2.addStretch(1)
        label.setNum(dial.value())
        dial.valueChanged.connect(label.setNum)
        #dial.valueChanged.connect(self.change_polar12)
        #self.change_polar12(dial.value())
        
        hbox.addWidget(dial)
        hbox.addLayout(vbox2) 
        vbox.addLayout(hbox)
        
        # adds coordinate controls to grid
        group_box.setLayout(vbox)  
        grid.addWidget(group_box, 0,0,2,1)
        grid.setColumnStretch(0, 1)
           
        '''
        start button
        '''
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.start_button = QPushButton("START", self)
        self.start_button.setCheckable(True)
        self.start_button.setStyleSheet("background-color : lightgreen")
        self.start_button.setFont(QFont('Times', 24))
        self.start_button.setFixedHeight(90)
        self.start_button.setFixedWidth(300)
        #self.start_button.clicked.connect(self.start_progres)
        hbox.addStretch(1)
        hbox.addWidget(self.start_button)
        hbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        grid.addLayout(vbox, 1, 1)
          
        '''
        file paths
        '''
        group_box = QGroupBox("File Paths")
        vbox = QVBoxLayout()
        label = QLabel("Model file path:")
        vbox.addWidget(label)
        self.model_file_label = QLabel("Not set...")
        vbox.addWidget(self.model_file_label)
        label = QLabel("Save file path:")
        vbox.addWidget(label)
        self.save_file_label = QLabel("Not set...")
        vbox.addWidget(self.save_file_label)      
        group_box.setLayout(vbox)  
        grid.addWidget(group_box, 0,1)
        grid.setColumnStretch(1, 2)
        
        
        # finally adds everything to the tab1
        self.setLayout(grid)


      