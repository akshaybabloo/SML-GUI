import logging
import os
import sys

import click
from PyQt5 import uic, QtWidgets, QtGui, QtCore

from utility import select_folder

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

    def closeEvent(self, a0: QtGui.QCloseEvent):
        logger.info("Exiting. Bye!")


@click.command()
@click.option('--debug', default=0, help="Verbose logging. Defaults to 0, add 1 for verbose logging.")
def main(debug):
    """
    Runs the main app, if ``--debug=1`` a more verbose logging is shown.

    Parameters
    ----------
    debug: int
        Verbose logging.
    """
    if debug == 1:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
