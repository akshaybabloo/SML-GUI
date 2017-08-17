"""
Custom widgets for the GUI
"""

from PyQt5 import QtWidgets, QtCore


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, narray, parent=None):
        super(TabWidget, self).__init__(parent)

        tablist = []
        layoutlist = []
        self.tablelist = []
        self.setMinimumHeight(150)
        self.setMinimumWidth(400)

        num_tab_widgets = narray.shape[0]

        for i in range(num_tab_widgets):
            tablist.append(QtWidgets.QWidget())
            self.addTab(tablist[i], str('Sample %s' % i))
            self.tablelist.append(QtWidgets.QTableView())
            setattr(self, 'Table%d' % i, self.tablelist[i])
            layoutlist.append(QtWidgets.QVBoxLayout())

            model = NumpyModel(narray[i])
            self.tablelist[i].setModel(model)

            layoutlist[i].addWidget(self.tablelist[i])
            tablist[i].setLayout(layoutlist[i])


class NumpyModel(QtCore.QAbstractTableModel):
    """
    Adds 2D numpy array to the ``QTableView``
    """

    def __init__(self, narray, headers=None, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._array = narray

        if headers is not None:
            self.header_labels = headers
        else:
            self.header_labels = [str(i) for i in range(self._array.shape[1])]

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
