"""
Utility for pre-processing the file before sending it to ``processor``.
"""
from __future__ import print_function

try:
    import configparser as configparser
except ImportError:
    import ConfigParser as configparser
    pass

import csv
import logging
import os
import platform
import re
import sys
from contextlib import contextmanager

import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from sklearn.model_selection import train_test_split

from smlgui.processor import check_files

logger = logging.getLogger(__name__)

__all__ = ['ReadCSV', 'is_windows', 'is_linux', 'is_mac', 'is_python3', 'select_folder', 'load_stylesheet',
           'loading_effects_context', 'loading_effects_decorator', 'get_sml_conf', 'write_sml_config']


class ReadCSV:
    """Read CSV files.

    This class reads in the CSV files starting with sam_*.csv, where * is the number.
    """

    def __init__(self, data):
        """

        Parameters
        ----------
        data
            Location of samples (folder location).

        Note
        -----

        If you are manually giving the location of the folder to ``data_folder`` option, you can ignore ``location`` option.
        """

        self.data_folder = data + os.sep
        if os.path.isdir(self.data_folder):
            self.prefixed = [filename for filename in os.listdir(self.data_folder) if filename.startswith("sam")]
        else:
            raise IOError('Data files not found')

        if len(self.prefixed) is 1:
            raise NotEnoughDataError("There should be more than one sample to continue.")

    def read_samples(self):
        """Read samples

        This method reads the files and indexes according to their sam_* number.

        Examples
        --------

        >>> files = ReadCSV()
        >>> files.read_samples()
        [[[...][...][...]]
        ...
        [[...][...][...]]]

        Returns
        -------
        flow  :  narray
        """
        self.prefixed.sort(key=natural_keys)  # Sorted with filename and sample number

        temp = [self.data_folder + self.prefixed for self.prefixed in self.prefixed]
        data = [np.genfromtxt(f, delimiter=",") for f in temp]
        data = np.asarray(data)

        return data

    def get_split_data(self, split_to=0.5):
        """Get split data for training and testing.

        Parameters
        ----------

        split_to
            Percentage split of data.

        Returns
        -------
        flow  :  dict
            Returns a dictionary of two``DataFrame``, and one ``float``.

        Examples
        --------

        >>> files = ReadCSV()
        >>> files.get_split_data()
        {'test_data': DataFrame,
         'train_data': DataFrame,
         'full_data': DataFrame,
         'training_split': float}
        """
        data = self.read_samples()

        if split_to > 1:
            raise SplitDataException("Split data should be less that 1.0")

        train, test = train_test_split(data, test_size=split_to)

        flow = {'test_data': test, 'train_data': train, 'full_data': data, 'training_split': split_to}

        return flow

    def sample_size(self):
        """
        Returns the length of the sample size.

        Returns
        -------

        flow  :  int
            Size of the list of sample names.
        """
        flow = len(self.prefixed)
        return flow

    def time_feature_length(self):
        """
        Returns the time length of a file by counting it's number of columns.

        Returns
        -------

        flow  :  dict
            Returns a dictionary with the following:

            - ``time_length`` - Time length of a sample as *int*.
            - ``feature_length`` - Feature length of a sample as *int*
        """
        file = self.prefixed[0]
        a = []
        with open(self.data_folder + file) as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            for col in reader:
                a.append(col)
        csv_file.close()

        flow = {'time_length': len(a), 'feature_length': len(a[0][0].split(','))}
        return flow

    def get_feature_names(self):
        """
        Reads feature names if present

        Returns
        -------

        flow  :  dict
            The dictionary contains the following:

            - ``number_of_features`` - Number of features as *int*
            - ``name_features`` - Feature names as *list*
        """

        names = []
        number_of_features = 0
        if os.path.isfile(self.data_folder + 'feature_names_eeg.txt'):
            try:
                with open(self.data_folder + 'feature_names_eeg.txt', 'r') as f:
                    data = f.read()
                f.close()
                names = data.split('\n')
                number_of_features = len(names)
            except IOError as e:
                print("file not found - ", e)
        else:
            with open(self.data_folder + self.prefixed[0]) as f:
                number_of_features = len(f.readline().split(','))
                for x in range(1, number_of_features + 1):
                    names.append("feature {}".format(x))
                f.close()

        flow = {'number_of_features': number_of_features, 'name_features': names}
        return flow

    def _get_class_labels(self):
        """
        Gets all the target class labels.

        Returns
        -------

        flow  :  list
            List of feature names if given or it is self generated.
        """
        flow = []
        if os.path.isfile(self.data_folder + 'tar_class_labels.csv'):
            with open(self.data_folder + 'tar_class_labels.csv', 'r') as csv_file:
                reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
                for row in reader:
                    flow.append(int(row[0]))
                csv_file.close()
        else:
            for temp in range(len(self.prefixed)):
                flow.append(1)

        return flow


def is_python3():
    """
    Check for Python 3

    >>> print(is_python3())
    True or False

    Returns
    -------
    bool: bool
        True or False
    """
    if sys.version_info[:2] >= (3, 5):
        return True
    else:
        return False


def atoi(text):
    """
    Checks if the file names contain numbers.

    Parameters
    ----------
    text
        This parameter could be a str or int.

    Returns
    -------

    flow  :  int, str
    """
    flow = int(text) if text.isdigit() else text
    return flow


def natural_keys(text):
    """
    Splits the number from the file name.

    Parameters
    ----------
    text
        A str parameter with number should be give, so the this method could split the contents.

    Returns
    -------
    flow  :  list
        List of strings.
    """
    flow = [atoi(c) for c in re.split('(\d+)', text)]
    return flow


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

    >>> print(is_windows())
    True or False

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

    >>> print(is_mac())
    True or False

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

    >>> print(is_linux())
    True or False

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

    f = QtCore.QFile(":darkstyle/style.qss")
    if not f.exists():
        logger.error("Unable to load stylesheet, file not found in "
                     "resources")
        return ""
    else:
        f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        ts = QtCore.QTextStream(f)
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


def loading_effects_decorator(func):
    """
    Decorator for creating an loading cursor.

    >>> @loading_effects_decorator
    >>> def do_lengthy_process():
    >>>     # DO something
    >>>     pass

    Parameters
    ----------
    func: function

    Returns
    -------
    new_function: object

    """

    def new_function(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            func(self)
        except Exception as e:
            raise e
            print("Error {}".format(e.args[0]))
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    return new_function


@contextmanager
def loading_effects_context():
    """
    Using context manager to create loading cursor for snippets of code.

    >>> with loading_effects_context():
    >>>     # Do something
    >>>     pass
    """
    try:
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        yield
    finally:
        QtWidgets.QApplication.restoreOverrideCursor()


def get_sml_conf():
    """
    Reads configuration file ``sml.conf`` if exists, else it creates one.

    Returns
    -------
    config: object
        ConfigParser object.
    """
    sml_conf_file = os.path.expanduser('~' + os.sep + 'sml.conf')

    config = configparser.ConfigParser()

    if os.path.isfile(sml_conf_file):
        config.read(sml_conf_file)
        return config
    else:
        config['DEFAULT'] = {'dark_mode': "true"}
        with open(sml_conf_file, 'w') as config_file:
            config.write(config_file)

        config.read(sml_conf_file)

        logger.info('sml.conf not found. Configuration file created at ' + sml_conf_file)
        return config


def write_sml_config(content):
    """
    Write configurations to ``sml.conf``

    Parameters
    ----------
    content: object
        ConfigParser object
    """
    sml_conf_file = os.path.expanduser('~' + os.sep + 'sml.conf')

    if os.path.isfile(sml_conf_file):
        with open(sml_conf_file, 'w') as config_file:
            content.write(config_file)
    else:
        raise ConfigFileNotFound("Make sure Config file is available at " + sml_conf_file)


####################################################################
#                                                                  #
#                           Exceptions                             #
#                                                                  #
####################################################################


class NotEnoughDataError(Exception):
    def __init__(self, message, errors=None):
        super(NotEnoughDataError, self).__init__(message)

        self.errors = errors


class SplitDataException(Exception):
    def __init__(self, message, errors=None):
        super(SplitDataException, self).__init__(message)

        self.errors = errors


class ConfigFileNotFound(Exception):
    def __init__(self, message, errors=None):
        super(ConfigFileNotFound, self).__init__(message)

        self.errors = errors
