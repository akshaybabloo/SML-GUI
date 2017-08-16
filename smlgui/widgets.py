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
