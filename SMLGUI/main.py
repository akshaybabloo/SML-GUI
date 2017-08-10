import logging
import os
import sys

import click
from PyQt5 import uic, QtWidgets, QtGui, QtCore

from smlgui.utility import select_folder
from smlgui import __version__

logger = logging.getLogger(__name__)


class AboutUi(QtWidgets.QDialog):
    """
    Open's ``AboutUi`` GUI.
    """

    def __init__(self):
        super(AboutUi, self).__init__()
        uic.loadUi(os.path.abspath('SMLGUI' + os.sep + 'gui' + os.sep + 'about.ui'), self)
        content = """
        Copyright Akshay Raj Gollahalli. Licensed under MIT. <br><br>
        
        Spikes Markup Language (SML) Exporter <br><br>
        
        <b>Third party software:</b><br><br>
        
        Python<br>
        Click<br>
        PyQT5<br>
        QT
        """

        self.setWindowTitle("AboutUi")
        self.setWindowIcon(
            QtGui.QIcon(os.path.abspath('SMLGUI' + os.sep + 'gui' + os.sep + 'assets' + os.sep + 'logo.png')))
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Focus on this window.

        self.textBrowser.setHtml(content)
        spikes_logo = QtGui.QPixmap(
            os.path.abspath('SMLGUI' + os.sep + 'gui' + os.sep + 'assets' + os.sep + 'spikes-logo.png'))
        self.logo.setPixmap(spikes_logo.scaled(99, 39, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation))
        self.version.setText("Version: " + __version__)

        logger.info("AboutUi GUI started.")
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        logger.info("Exiting AboutUi.")


class Ui(QtWidgets.QMainWindow):
    """
    Main class that loads and runs the ``main.ui``.
    """

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(os.path.abspath('SMLGUI' + os.sep + 'gui' + os.sep + 'main.ui'), self)
        self.status_message = "Welcome to SML Exporter!"

        self.messageBar.showMessage(self.status_message)
        self.setWindowIcon(
            QtGui.QIcon(os.path.abspath('SMLGUI' + os.sep + 'gui' + os.sep + 'assets' + os.sep + 'logo.png')))
        self.setFixedSize(self.size())

        # Connections and events
        self.load_samples_button.clicked.connect(select_folder)
        self.load_samples_button.installEventFilter(self)

        self.about_menu.triggered.connect(self.show_about)

        logger.info("Main GUI started")
        # showing the app gui to user
        self.show()

    @staticmethod
    def show_about():
        app = AboutUi()
        app.exec_()

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
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
