from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
import sys
import os


class Ui(QtWidgets.QMainWindow):
    """
    Main class that loads and runs the ``main.ui``.
    """

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('gui' + os.sep + 'main.ui', self)

        # showing the app gui to user
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
