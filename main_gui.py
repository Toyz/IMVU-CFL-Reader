__author__ = 'Toyz'

import os
import sys
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, uic
from imvu.cfl.CFL import CFL
from imvu.chkn.ChknFile import ChknFile


form_class = uic.loadUiType("interface/main.ui")[0]

class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.actionOpen_CFL.triggered.connect(self.OpenCFLClicked)
        self.actionConvert_to_CHKN.triggered.connect(self.convertToCHKNClicked)
        self.actionExtract_All.triggered.connect(self.extractAllFileClicked)

    def extractAllFileClicked(self):
        if len(self.files) <= 0:
            return

        file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))

        if len(file) <= 0:
            return

        for name, data in self.files.iteritems():
            open(os.path.join(file, name), "wb").write(data)

        QMessageBox.information(self,
                                "Information",
                                "Extracted to: " + file)

    def convertToCHKNClicked(self):
        if len(self.files) <= 0:
            return

        chknfile = QtGui.QFileDialog.getSaveFileName(self, 'Export to CHKN', './', "CHKN  File (*.chkn)")

        if len(chknfile) <= 0:
            return

        chknfile = str(chknfile)

        chkn = ChknFile(open(chknfile, "wb"), "w")

        for name, data in self.files.iteritems():
            chkn.writestr(name, data)

        QMessageBox.information(self,
                                "Information",
                                "Save CHKN file to \n" + chknfile)
        chkn.close()

    def OpenCFLClicked(self):
        cflfile = QtGui.QFileDialog.getOpenFileName(self, 'Open CFL file', './', "CFL File (*.cfl)")

        if len(cflfile) <= 0:
            return

        cflfile = str(cflfile)

        cfl = CFL(cflfile)
        head, tail = os.path.split(cflfile)

        self.cflFilesList.clear()
        self.files = {}
        for name in cfl.getEntryNames():
            item = QListWidgetItem(name)
            self.cflFilesList.addItem(item)
            self.files[name] = cfl.getContents(name)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.setWindowFlags(myWindow.windowFlags() | QtCore.Qt.CustomizeWindowHint)
    myWindow.setWindowFlags(myWindow.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
    myWindow.show()
    app.exec_()
