"""
Custom widgets for the GUI
"""

from PyQt5 import QtWidgets


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)

        tablist = []
        tablabellist = []
        layoutlist = []
        self.tablelist = []
        self.setMinimumHeight(150)
        self.setMinimumWidth(400)

        headerlist = ['ID', 'Question', 'Answer 1', 'Answer 2', 'Answer 3', 'Difficulty', 'Statistics', 'Date Added',
                      'Added By', 'Date Modified']

        num_tab_widgets = 10

        for i in range(num_tab_widgets):
            tablist.append(QtWidgets.QWidget())
            self.addTab(tablist[i], str('Sample %s' % i))
            # tablabellist.append(QtWidgets.QLabel('title'))
            self.tablelist.append(QtWidgets.QTableWidget())
            setattr(self, 'Table%d' % i, self.tablelist[i])
            layoutlist.append(QtWidgets.QVBoxLayout())

            self.tablelist[i].setColumnCount(len(headerlist))
            self.tablelist[i].setHorizontalHeaderLabels(headerlist)
            self.tablelist[i].setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.tablelist[i].setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
            self.tablelist[i].setSelectionMode(QtWidgets.QTableWidget.SingleSelection)

            # layoutlist[i].addWidget(tablabellist[i])
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
