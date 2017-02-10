#encoding: utf-8
from PyQt5.QtWidgets import QMainWindow, QWidget, QHeaderView,QTableWidgetItem
from editor import Ui_editor
from PyQt5.QtCore import QCoreApplication

class EditorDialog(QWidget, Ui_editor):


    def __init__(self,parent=None,okFunc=None):
        super().__init__(parent=parent)

        self.okFunc = okFunc

        # setup UI from Designer
        self.setupUi(self)
        self.okButton.clicked.connect(self.okClicked)
        self.plusButton.clicked.connect(self.addRow)
        self.minusButton.clicked.connect(self.removeRow)
        self.table.clicked.connect(lambda: self.onTableClicked())
# https://stackoverflow.com/questions/38098763/pyside-pyqt-how-to-make-set-qtablewidget-column-width-as-proportion-of-the-a
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        QCoreApplication.instance().installEventFilter(self);


    def onTableClicked(self):
        print("currentRow = ",self.table.currentRow())
        if self.table.currentRow() != -1:
            self.minusButton.setEnabled(True)
        else:
            self.minusButton.setEnabled(False)


    def removeRow(self):
        selectedRow = self.table.currentRow()
        self.table.removeRow(selectedRow)

    def addRows(self,configObject):
        map = configObject.configMap
        i = 0
        for key in map:
            self.table.insertRow(i)
            self.table.setItem(i , 0, QTableWidgetItem(key))
            self.table.setItem(i , 1, QTableWidgetItem(map[key]))

    def addRow(self):
        rowCount = self.table.rowCount()
        self.table.insertRow(rowCount)

    def removeAllRows(self):
        while self.table.rowCount() != 0:
            self.table.removeRow(0)


    def showWithRows(self,configObject):
        self.show()
        self.removeAllRows()
        self.addRows(configObject)

    def rowsToMap(self):
        myMap = {}
        for i in range(0, self.table.rowCount()):
            key = self.table.item(i,0).text()
            value = self.table.item(i,1).text()
            myMap[key] = value
        return myMap


    def okClicked(self):
        self.close()
        if self.okFunc != None:
            self.okFunc(self.rowsToMap())

    def setOnOkClicked(self, func):
        self.okFunc = func
