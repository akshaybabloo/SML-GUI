from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
import sys
import logging
import os
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger(__name__)


class Ui(QtWidgets.QMainWindow):
    """
    Main class that loads and runs the ``main.ui``.
    """

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('gui' + os.sep + 'main.ui', self)
        self.status_message = "Welcome to SML Exporter!"

        self.messageBar.showMessage(self.status_message)
        self.setWindowIcon(QtGui.QIcon('gui' + os.sep + 'assets' + os.sep + 'logo.png'))
        self.setFixedSize(self.size())

        logger.info("GUI started")
        # showing the app gui to user
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
