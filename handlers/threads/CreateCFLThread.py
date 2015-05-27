__author__ = 'Toyz'

from PyQt4 import QtCore, QtGui, uic
from handlers.cfl.CFLMaker import CFLMaker
import os

class CreateCFLThread(QtCore.QThread):
    def __init__(self, parent, cflfile, folder):
        QtCore.QThread.__init__(self, parent)
        self.cflfile = cflfile
        self.file = folder

    def run(self):
        cflmaker = CFLMaker(self.cflfile)

        total = len([name for name in os.listdir(self.file) if os.path.isfile(os.path.join(self.file, name))])
        self.emit(QtCore.SIGNAL("total(PyQt_PyObject)"), total)
        start = 1
        for i in os.listdir(self.file):
            if os.path.isfile(os.path.join(self.file, i)):
                # self.__progressui.setText(i)
                self.emit(QtCore.SIGNAL("setText(PyQt_PyObject)"), "Adding: " + i)
                f = open(os.path.join(self.file, i), "rb")
                cflmaker.store(i, str(f.read()))
                f.close()
                self.emit(QtCore.SIGNAL("update(PyQt_PyObject)"), start)
                print str(total) + " - " + str(start)
                start += 1

        cflmaker.finish()

        self.emit(QtCore.SIGNAL("openCFL(PyQt_PyObject)"), self.cflfile)
        self.emit(QtCore.SIGNAL("sendMessage(PyQt_PyObject, PyQt_PyObject)"), "Information",
                  "Saved CFL file saved to \n" + self.cflfile)
        self.emit(QtCore.SIGNAL("setText(PyQt_PyObject)"), "Finished")
        # QMessageBox.information(self,
        #                        "Information",
        #                        "Save CFL file saved to \n" + self.cflfile)
