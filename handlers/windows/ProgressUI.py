from handlers.tools import Utils
from handlers.tools.temploader import TempLoad

__author__ = 'Toyz'

from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, uic

loader = TempLoad("ui.cfl")

form_class = uic.loadUiType(loader.getfile("progress.ui"))[0]


class ProgressUI(QtGui.QDialog, form_class):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.n = 0

    def setProgress(self, amount):
        self.progressBar.setValue(amount)

    def setText(self, text):
        if len(text) > 75:
            text = Utils.Utils.trunc(text)

        self.label.setText(text)

    def update(self, amount):
        self.setProgress(amount)

    def total(self, total):
        self.progressBar.setMaximum(total)
