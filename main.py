import logging
import os
import sys

from PyQt5 import uic, QtWidgets, QtGui, QtCore

from utility import select_folder

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

        # Connections and events
        self.load_samples_button.clicked.connect(select_folder)
        self.load_samples_button.installEventFilter(self)

        logger.info("GUI started")
        # showing the app gui to user
        self.show()

    def eventFilter(self, objects, event):
        if objects.objectName() == 'load_samples_button':
            if event.type() == QtCore.QEvent.HoverEnter:
                self.messageBar.showMessage("Loads all samples starting with sam1_*.csv")
                return True
            elif event.type() == QtCore.QEvent.HoverLeave:
                self.messageBar.showMessage(self.status_message)
                return True

        return False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
