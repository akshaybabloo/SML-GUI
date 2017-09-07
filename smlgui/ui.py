"""
UI class to control the visibility, usability and control of GUI.
"""
import logging
import os

import numpy as np
from PyQt5 import uic, QtWidgets, QtGui, QtCore

from smlgui import __version__
from smlgui.utility import select_folder, loading_effects_decorator, get_sml_conf, write_sml_config, \
    loading_effects_context, ReadCSV
from smlgui.widgets import TabWidget, CustomQMainWidget, CustomQDialog

__all__ = ['AboutUi', 'HomeUi', 'PreferenceUi', 'ImportUi', 'ExportUi']

logger = logging.getLogger(__name__)
conf = get_sml_conf()
dark_mode_check = QtCore.Qt.Checked if conf['DEFAULT']['dark_mode'] == "true" else QtCore.Qt.Unchecked


class AboutUi(CustomQDialog):
    """
    Open's ``AboutUi`` GUI.
    """

    def __init__(self):
        super(AboutUi, self).__init__()
        uic.loadUi(os.path.abspath('smlgui' + os.sep + 'gui' + os.sep + 'about.ui'), self)
        content = """
        Copyright Akshay Raj Gollahalli. Licensed under MIT. <br><br>

        Spikes Markup Language (SML) Maker <br><br>

        <b>Libraries that made it all possible:</b><br><br>

        Python<br>
        Click<br>
        PyQT5<br>
        QT<br>
        NumPy
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


class PreferenceUi(CustomQDialog):
    """
    Open ``preference`` pane.
    """

    def __init__(self, parent=None):
        global dark_mode_check

        super(PreferenceUi, self).__init__(parent)
        uic.loadUi(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'preference.ui', self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(
            QtGui.QIcon(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'assets' + os.sep + 'logo.png'))

        self.ok_button.clicked.connect(self.on_ok)

        self.dark_mode_check.setTristate(False)
        self.dark_mode_check.setCheckState(dark_mode_check)

    def on_ok(self):
        """
        Event for ``Ok` button.
        """
        global dark_mode_check, conf

        if self.dark_mode_check.isChecked():
            if dark_mode_check is not QtCore.Qt.Checked:
                dark_mode_check = QtCore.Qt.Checked
            if conf['DEFAULT']['dark_mode'] != "true":
                conf.set('DEFAULT', 'dark_mode', 'true')
                write_sml_config(conf)
                QtWidgets.QMessageBox.warning(self, "SML Maker", "Restart SML Maker to make changes.")
        else:
            dark_mode_check = QtCore.Qt.Unchecked
            conf.set('DEFAULT', 'dark_mode', 'false')
            write_sml_config(conf)
            QtWidgets.QMessageBox.information(self, "SML Maker", "Restart SML Maker to make changes.")


class ImportUi(CustomQMainWidget):
    """
    Imports SML and exports to CSV.
    """

    def __init__(self, parent=None):
        super(ImportUi, self).__init__(parent)

        uic.loadUi(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'import.ui', self)
        self.status_message = "Welcome to SML Importer!"

        self.setWindowTitle("SML Importer")
        self.messageBar.showMessage(self.status_message)
        self.setWindowIcon(
            QtGui.QIcon(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'assets' + os.sep + 'logo.png'))

        my_font = QtGui.QFont()
        my_font.setBold(True)
        my_font.setPixelSize(50)

        # Text before loading the samples
        self.temp_text_table = QtWidgets.QLabel()
        self.temp_text_table.setText("Load SML")
        self.temp_text_table.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.temp_text_table.setFont(my_font)
        self.temp_text_table.setMinimumHeight(150)
        self.temp_text_table.setMinimumWidth(400)

        # Text before loading the samples
        self.temp_text_stats = QtWidgets.QLabel()
        self.temp_text_stats.setText("Load SML")
        self.temp_text_stats.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.temp_text_stats.setFont(my_font)
        self.temp_text_stats.setMinimumHeight(150)
        self.temp_text_stats.setMinimumWidth(800)

        self.table_layout.addWidget(self.temp_text_table)
        self.stats_layout.addWidget(self.temp_text_stats)
        self.samples_to_csv.setEnabled(False)
        self.weights_to_csv.setEnabled(False)
        self.connections_to_csv.setEnabled(False)
        self.spikes_to_csv.setEnabled(False)
        self.encoded_to_csv.setEnabled(False)

        # GUI
        self.load_sml_button.clicked.connect(self.load_table)
        self.about_menu.triggered.connect(self.show_about)

        logger.info("Exporter GUI started")

    @loading_effects_decorator
    def load_table(self):
        """
        Populates the ``samples`` table.
        """
        self.temp_text_table.deleteLater()
        table_widget = TabWidget(np.random.randn(60, 128, 14))
        self.table_layout.addWidget(table_widget)

    @staticmethod
    def show_about():
        """
        Opening ``AboutUi``
        """
        app = AboutUi()
        app.exec_()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        logger.info("Exiting ImportUi")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)


class ExportUi(CustomQMainWidget):
    """
    Main class that loads and runs the ``export.ui``.
    """

    def __init__(self, parent=None):
        super(ExportUi, self).__init__(parent)
        uic.loadUi(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'export.ui', self)
        self.status_message = "Welcome to SML Exporter!"

        self.setWindowTitle("SML Exporter")
        self.messageBar.showMessage(self.status_message)
        self.setWindowIcon(
            QtGui.QIcon(os.getcwd() + os.sep + 'smlgui' + os.sep + 'gui' + os.sep + 'assets' + os.sep + 'logo.png'))

        my_font = QtGui.QFont()
        my_font.setBold(True)
        my_font.setPixelSize(50)

        # Text before loading the samples
        self.temp_text_table = QtWidgets.QLabel()
        self.temp_text_table.setText("Load Files")
        self.temp_text_table.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.temp_text_table.setFont(my_font)
        self.temp_text_table.setMinimumHeight(150)
        self.temp_text_table.setMinimumWidth(400)

        # Text before loading the samples
        self.temp_text_stats = QtWidgets.QLabel()
        self.temp_text_stats.setText("Load Files")
        self.temp_text_stats.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.temp_text_stats.setFont(my_font)
        self.temp_text_stats.setMinimumHeight(150)
        self.temp_text_stats.setMinimumWidth(500)

        # Connections and events
        self.load_samples_button.clicked.connect(self.load_table)
        self.load_samples_button.installEventFilter(self)

        self.stats_layout.addWidget(self.temp_text_stats)
        self.table_layout.addWidget(self.temp_text_table)
        self.about_menu.triggered.connect(self.show_about)

        logger.info("Main GUI started")

    def load_table(self):
        """
        Populates the ``samples`` table.
        """
        location = select_folder()
        read_csv = ReadCSV(location)

        with loading_effects_context():
            try:
                self.temp_text_table.deleteLater()
            except Exception:
                pass

            # Remove if QTabWidget already exists.
            for a in range(self.table_layout.count()):
                if isinstance(self.table_layout.itemAt(a).widget(), QtWidgets.QTabWidget):
                    self.table_layout.itemAt(a).widget().deleteLater()

            table_widget = TabWidget(read_csv.read_samples())
            self.table_layout.addWidget(table_widget)

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
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)


class HomeUi(CustomQMainWidget):
    """
    Main class that loads and runs the ``main.ui``.
    """

    def __init__(self, parent=None):
        super(HomeUi, self).__init__(parent)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)  # Frameless window
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
        self.preference_menu.triggered.connect(self.show_preference)
        self.exit_menu.triggered.connect(self.close)

        self.export_ui = ExportUi()
        self.import_ui = ImportUi()

        logger.info("HomeUi GUI started")
        # showing the app gui to user
        self.show()

    @staticmethod
    def show_about():
        """
        Opening ``AboutUi``
        """
        app = AboutUi()
        app.exec_()

    @staticmethod
    def show_preference():
        """
        Opening ``AboutUi``
        """
        app = PreferenceUi()
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
