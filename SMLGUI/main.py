import logging
import os
import sys

import click
from PyQt5 import uic, QtWidgets, QtGui, QtCore

from smlgui import __version__
from smlgui.utility import select_folder, is_windows
from smlgui.widgets import TabWidget

logger = logging.getLogger(__name__)


class AboutUi(QtWidgets.QDialog):
    """
    Open's ``AboutUi`` GUI.
    """

    def __init__(self):
        super(AboutUi, self).__init__()
        uic.loadUi(os.path.abspath('smlgui' + os.sep + 'gui' + os.sep + 'about.ui'), self)
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
            QtGui.QIcon(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'assets' + os.sep + 'logo.png'))
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Focus on this window.

        self.textBrowser.setHtml(content)
        spikes_logo = QtGui.QPixmap(
            os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'assets' + os.sep + 'spikes-logo.png')
        self.logo.setPixmap(spikes_logo.scaled(99, 39, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation))
        self.version.setText("Version: " + __version__)

        logger.info("AboutUi GUI started.")
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        logger.info("Exiting AboutUi.")


class ImportUi(QtWidgets.QMainWindow):
    """
    Note yet implemented.
    """

    def __init__(self, parent=None):
        super(ImportUi, self).__init__(parent)

        uic.loadUi(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'import.ui', self)
        self.status_message = "Welcome to SML Exporter!"

        self.messageBar.showMessage(self.status_message)
        self.setWindowIcon(
            QtGui.QIcon(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'assets' + os.sep + 'logo.png'))

        self.table_widget = TabWidget()
        self.table_layout.addWidget(self.table_widget)

        logger.info("Exporter GUI started")

    def closeEvent(self, a0: QtGui.QCloseEvent):
        logger.info("Exiting ImportUi")


class ExportUi(QtWidgets.QMainWindow):
    """
    Main class that loads and runs the ``export.ui``.
    """

    def __init__(self, parent=None):
        super(ExportUi, self).__init__(parent)
        uic.loadUi(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'export.ui', self)
        self.status_message = "Welcome to SML Maker!"

        self.messageBar.showMessage(self.status_message)
        self.setWindowIcon(
            QtGui.QIcon(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'assets' + os.sep + 'logo.png'))

        # Connections and events
        self.load_samples_button.clicked.connect(select_folder)
        self.load_samples_button.installEventFilter(self)

        self.about_menu.triggered.connect(self.show_about)

        logger.info("Main GUI started")

    @staticmethod
    def show_about():
        """
        Opens ``AboutUi``
        """
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
        logger.info("Exiting ExportUi")


class Home(QtWidgets.QMainWindow):
    """
    Main class that loads and runs the ``main.ui``.
    """

    def __init__(self, parent=None):
        super(Home, self).__init__(parent)
        uic.loadUi(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'home.ui', self)
        self.status_message = "Welcome to SML Maker!"

        self.messageBar.showMessage(self.status_message)
        self.setWindowIcon(
            QtGui.QIcon(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'assets' + os.sep + 'logo.png'))

        # Connections and events
        self.export_button.clicked.connect(self.show_export_ui)
        self.import_button.clicked.connect(self.show_import_ui)

        self.export_button.installEventFilter(self)
        self.import_button.installEventFilter(self)

        self.about_menu.triggered.connect(self.show_about)
        self.exit_menu.triggered.connect(self.close)

        self.export_ui = ExportUi()
        self.import_ui = ImportUi()

        logger.info("Home GUI started")
        # showing the app gui to user
        self.show()

    @staticmethod
    def show_about():
        """
        Opening ``AboutUi``
        """
        app = AboutUi()
        app.exec_()

    def show_export_ui(self):
        """
        Opening ``ExportUi``
        """
        self.export_ui.show()
        self.close()

    def show_import_ui(self):
        """
        Opening ``ImportUi``
        """
        self.import_ui.show()
        self.close()

    def eventFilter(self, objects, event):
        if objects.objectName() == 'export_button':
            if event.type() == QtCore.QEvent.HoverEnter:
                self.messageBar.showMessage("Export all your data to SML file.")
                return True
            elif event.type() == QtCore.QEvent.HoverLeave:
                self.messageBar.showMessage(self.status_message)
                return True
        elif objects.objectName() == 'import_button':
            if event.type() == QtCore.QEvent.HoverEnter:
                self.messageBar.showMessage("Import SML and export it to CSV, JSON or Text.")
                return True
            elif event.type() == QtCore.QEvent.HoverLeave:
                self.messageBar.showMessage(self.status_message)
                return True

        return False

    def closeEvent(self, a0: QtGui.QCloseEvent):
        logger.info("Exiting. Bye!")


@click.command()
@click.option('--debug', is_flag=True, help="Verbose logging. Defaults to 0, add 1 for verbose logging.")
@click.option('--verbose',is_flag=True, help="Verbose logging.")
@click.option('--version', '-v', is_flag=True, help="Show the version number.")
def main(debug, verbose, version):
    """
    Runs the main app, if ``--debug=1`` a more verbose logging is shown.

    Parameters
    ----------
    version
    verbose
    debug: int
        Verbose logging.
    """
    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    elif debug:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d: %(message)s')
    elif version:
        click.echo("Version " + __version__)
        sys.exit()

    if is_windows():
        import ctypes
        my_app_id = 'gollahalli.sml_gui.' + __version__
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    app = QtWidgets.QApplication(sys.argv)
    window = Home()
    f = open(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'assets' + os.sep + 'style.qss')
    app.setStyleSheet(f.read())
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
