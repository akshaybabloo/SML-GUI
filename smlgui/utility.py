"""
Utility for pre-processing the file before sending it to ``processor``.
"""
import logging
import sys
import platform

from PyQt5 import QtWidgets

from smlgui.processor import check_files

logger = logging.getLogger(__name__)


def select_folder():
    """
    Open's a QT QFileDialog and returns the path of the folder
    """
    logging.info("Select folder.")
    folder_location = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")

    check_files(folder_location)

    return folder_location


def is_windows():
    """
    Check if windows os

    Returns
    -------
    bool: bool
        True or False.

    """
    if sys.platform == 'win32':
        return True
    return False


def is_mac():
    """
    Check if mac os

    Returns
    -------
    bool: bool
        True or False.

    """
    if sys.platform == 'darwin':
        return True
    return False


def is_linux():
    """
    Check if linux os

    Returns
    -------
    bool: bool
        True or False.

    """
    if sys.platform == 'linux':
        return True
    return False


def load_stylesheet():
    """
    Load's the ``style.qss``.
    """
    # Smart import of the rc file
    import smlgui.gui.assets.style_rc

    # Load the stylesheet content from resources
    from PyQt5.QtCore import QFile, QTextStream

    f = QFile(":darkstyle/style.qss")
    if not f.exists():
        logger.error("Unable to load stylesheet, file not found in "
                        "resources")
        return ""
    else:
        f.open(QFile.ReadOnly | QFile.Text)
        ts = QTextStream(f)
        stylesheet = ts.readAll()
        if platform.system().lower() == 'darwin':  # see issue #12 on github
            mac_fix = '''
            QDockWidget::title
            {
                background-color: #31363b;
                text-align: center;
                height: 12px;
            }
            '''
            stylesheet += mac_fix
        return stylesheet

if __name__ == '__main__':
    print(load_stylesheet())