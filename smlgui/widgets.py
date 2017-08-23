"""
Custom widgets for the GUI
"""

from PyQt5 import QtWidgets, QtCore

__all__ = ['TabWidget', 'CustomQDialog', 'CustomQMainWidget']


class TabWidget(QtWidgets.QTabWidget):
    """
    Table widget to populate all the samples.
    """
    def __init__(self, n_array, parent=None):
        super(TabWidget, self).__init__(parent)

        tab_list = []
        layoutlist = []
        self.table_list = []
        self.setMinimumHeight(150)
        self.setMinimumWidth(400)

        num_tab_widgets = n_array.shape[0]

        for i in range(num_tab_widgets):
            tab_list.append(QtWidgets.QWidget())
            self.addTab(tab_list[i], str('Sample %s' % i))
            self.table_list.append(QtWidgets.QTableView())
            setattr(self, 'Table%d' % i, self.table_list[i])
            layoutlist.append(QtWidgets.QVBoxLayout())

            model = NumpyModel(n_array[i])
            self.table_list[i].setModel(model)

            layoutlist[i].addWidget(self.table_list[i])
            tab_list[i].setLayout(layoutlist[i])


class NumpyModel(QtCore.QAbstractTableModel):
    """
    Adds 2D numpy array to the ``QTableView``
    """

    def __init__(self, n_array, headers=None, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._array = n_array

        if headers is not None:
            self.header_labels = headers
        else:
            self.header_labels = [str(i+1) for i in range(self._array.shape[1])]

    def rowCount(self, parent=None):
        return self._array.shape[0]

    def columnCount(self, parent=None):
        return self._array.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                row = index.row()
                col = index.column()
                return QtCore.QVariant("%.5f" % self._array[row, col])
        return QtCore.QVariant()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.header_labels[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)


class CustomQMainWidget(QtWidgets.QMainWindow):
    """
    Custom ``QMainWidget``, that will (in future) implement frameless window.
    """
    def __init__(self, *args):
        super(CustomQMainWidget, self).__init__(*args)
        pass


class CustomQDialog(QtWidgets.QDialog):
    """
    Custom ``QDialog``, that will (in future) implement frameless window.
    """
    def __init__(self, *args):
        super(CustomQDialog, self).__init__(*args)
        pass
