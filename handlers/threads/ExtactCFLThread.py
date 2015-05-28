__author__ = 'Toyz'

from PyQt4 import QtCore
import os


class ExtractCFLThread(QtCore.QThread):
    def __init__(self, parent, cfl, output):
        QtCore.QThread.__init__(self, parent)
        self.items = cfl
        self.output = output

    def run(self):
        itemLength = len(self.items)
        self.emit(QtCore.SIGNAL("total(PyQt_PyObject)"), itemLength)

        start = 1
        for key, data in self.items.iteritems():
            self.emit(QtCore.SIGNAL("setText(PyQt_PyObject)"), "Extracting: " + key)
            f = open(os.path.join(self.output, key), "wb")
            f.write(data)
            f.close()
            self.emit(QtCore.SIGNAL("update(PyQt_PyObject)"), start)
            start += 1

        self.emit(QtCore.SIGNAL("sendMessage(PyQt_PyObject, PyQt_PyObject)"), "Information",
                  "Extracted Items too \n" + self.output)
        self.emit(QtCore.SIGNAL("setText(PyQt_PyObject)"), "Finished")
