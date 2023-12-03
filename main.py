

from PyQt5.QtWidgets import QApplication
import sys
from src.front_end.main_window import GUI
from src.front_end.utils import Message


def excepthook(exc_type, exc_value, exc_tb):
    msg = f'An uncaught exception has occurred!\n\n{str(exc_value)}'
    msg_dialog = Message(msg=msg, type='critical', buttons='y')
    msg_dialog.exec_()

def main():
    #sys.excepthook = excepthook
    global qapp
    qapp = QApplication(sys.argv)
    gui = GUI()
    sys.exit(qapp.exec_()) # Start the Qt event loop end exit after it stops
    
    
if __name__ == '__main__':
    main()