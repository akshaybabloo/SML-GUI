"""
Utility for pre-processing the file before sending it to ``processor``.
"""
import logging

from PyQt5 import QtWidgets

from processor import check_files

logger = logging.getLogger(__name__)


def select_folder():
    """
    Open's a QT QFileDialog and returns the path of the folder
    """
    logging.info("Select folder.")
    folder_location = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")

    check_files(folder_location)
