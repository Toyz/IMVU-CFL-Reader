from handlers.cfl.CFLMaker import CFLMaker
from handlers.tools import Utils

__author__ = 'Toyz'

import os
import sys
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, uic
from handlers.cfl.CFLOpener import CFLMaker
from handlers.chkn.ChknFile import ChknFile
from handlers.tools.temploader import TempLoad
import webbrowser

loader = TempLoad("ui.cfl")

form_class = uic.loadUiType(loader.getfile("main.ui"))[0]


class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        self.__selectedIndex = -1
        QtGui.QMainWindow.__init__(self, parent)
        self.files = {}
        self.setupUi(self)
        # set up images
        self.__imageFormats = {".jpg", ".png", ".gif", ".tif"}
        self.__imageIcon = QIcon(loader.getimage("image"))
        self.__fileIcon = QIcon(loader.getimage("file"))

        self.actionExtract_Single_File.setIcon(QIcon(loader.getimage("singleEx")))
        self.actionExtractSingle.setIcon(QIcon(loader.getimage("singleEx")))
        self.actionOpen.setIcon(QIcon(loader.getimage("open")))
        self.actionNew.setIcon(QIcon(loader.getimage("new")))
        self.actionExtract.setIcon(QIcon(loader.getimage("extract")))
        self.actionOpen_CFL.setIcon(QIcon(loader.getimage("open")))
        self.actionExtract_All.setIcon(QIcon(loader.getimage("extract")))
        self.actionCreate_CFL.setIcon(QIcon(loader.getimage("new")))
        self.actionQuit.setIcon(QIcon(loader.getimage("close")))
        self.actionConvert_to_CHKN.setIcon(QIcon(loader.getimage("convert")))
        # open buttons
        self.actionOpen_CFL.triggered.connect(self.OpenCFLClicked)
        self.actionOpen.triggered.connect(self.OpenCFLClicked)
        # convert buttons
        self.actionConvert_to_CHKN.triggered.connect(self.convertToCHKNClicked)
        # extract buttons
        self.actionExtract_All.triggered.connect(self.extractAllFileClicked)
        self.actionExtract.triggered.connect(self.extractAllFileClicked)
        self.actionExtract_Single_File.triggered.connect(self.extractOneFile)
        self.actionExtractSingle.triggered.connect(self.extractOneFile)
        # new Buttons
        self.actionCreate_CFL.triggered.connect(self.createCFLFromFolder)
        self.actionNew.triggered.connect(self.createCFLFromFolder)
        # close
        self.actionQuit.triggered.connect(self.Close)
        #help
        self.actionSource_Code_Github.triggered.connect(self.gotogithub)
        self.actionToyz_IMVU.triggered.connect(self.gotoimvu)

        # table events
        self.cflFilesList.cellClicked.connect(self.slotItemClicked)

    def gotogithub(self):
        webbrowser.open("https://github.com/Toyz/IMVU-CFL-Reader")

    def gotoimvu(self):
        webbrowser.open("http://avatars.imvu.com/Toyz")

    def extractOneFile(self):
        if self.__selectedIndex <= -1:
            return

        key = self.files.keys()[self.__selectedIndex]

        data = self.files[key]

        filesavelocaiton = str(QtGui.QFileDialog.getSaveFileName(self, 'Save File To', './' + key))
        if len(filesavelocaiton) <= 0:
            return

        f = open(filesavelocaiton, "wb")
        f.write(data)
        f.close()

        self.__selectedIndex = -1
        QMessageBox.information(self,
                                "Information",
                                "Saved file to \n" + filesavelocaiton)

    def slotItemClicked(self, item, item2):
        if len(self.files) <= 0:
            return

        self.__selectedIndex = item
        # print self.files.keys()[0]

    def Close(self):
        loader.clean()
        sys.exit()

    def createCFLFromFolder(self):
        file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory to make CFL"))

        if len(file) <= 0:
            return

        cflfile = str(QtGui.QFileDialog.getSaveFileName(self, 'Save CFL To', './', "CFL File (*.cfl)"))

        if len(cflfile) <= 0:
            return

        if os.path.isfile(cflfile):
            os.unlink(cflfile)

        cflMaker = CFLMaker(cflfile)

        for i in os.listdir(file):
            if os.path.isfile(os.path.join(file, i)):
                f = open(os.path.join(file, i), "rb")
                cflMaker.store(i, str(f.read()))
                f.close()

        cflMaker.finish()

        self.__openCFL(cflfile)
        QMessageBox.information(self,
                                "Information",
                                "Save CFL file saved to \n" + cflfile)

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

        self.cflFilesList.clear()
        self.__openCFL(cflfile)

    def __openCFL(self, cflfile):
        name = os.path.splitext(os.path.basename(cflfile))
        self.setWindowTitle("CFL Creator & Converter [" + name[0] + name[1] + "]")
        cfl = CFLMaker(cflfile)

        self.files = {}
        index = 0
        self.__selectedIndex = -1
        self.cflFilesList.setRowCount(len(cfl.getEntryNames()))
        for name in cfl.getEntryNames():
            fileName, fileExtension = os.path.splitext(name)
            if len(name) >= 75:
                newName = Utils.Utils.trunc(name, max_pos=110)
            else:
                newName = name
            cName = QTableWidgetItem(newName)
            cName.setFlags(QtCore.Qt.ItemIsEnabled)
            if fileExtension in self.__imageFormats:
                cName.setIcon(self.__imageIcon)
            else:
                cName.setIcon(self.__fileIcon)
            self.cflFilesList.setItem(index, 0, cName)

            cSize = QTableWidgetItem(Utils.Utils.sizeof_fmt(cfl.getFileSize(name)))
            cSize.setTextAlignment(4 | 80)
            cSize.setFlags(QtCore.Qt.ItemIsEnabled)
            self.cflFilesList.setItem(index, 1, cSize)
            self.files[name] = cfl.getContents(name)

            index += 1

        labels = QtCore.QStringList()
        labels.append('Filename')
        labels.append('File size')
        self.cflFilesList.setHorizontalHeaderLabels(labels)
        self.cflFilesList.resizeColumnsToContents()
        self.cflFilesList.resizeRowsToContents()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.setWindowFlags(myWindow.windowFlags() | QtCore.Qt.CustomizeWindowHint)
    myWindow.setWindowFlags(myWindow.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
    myWindow.show()
    app.exec_()
