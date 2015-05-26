__author__ = 'Toyz'

from handlers.cfl.CFL import CFL
import tempfile
import os

DEFAULT_FOLDER = "interface"
class TempLoad:
    def __init__(self, cfl):
        if self.__doesEixst(cfl):
            self.__loaded = CFL(cfl)
        self.__tempFiles = {}

    def GetFile(self, cfl):
        if self.__doesEixst(os.path.join(DEFAULT_FOLDER, cfl)):
            return os.path.join(DEFAULT_FOLDER, cfl)

        data = self.__loaded.getContents(cfl)
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(data)
        f.close()
        self.__tempFiles[cfl] = f.name
        return f.name

    def __doesEixst(self, cfl):
        return os.path.isfile(cfl)

    def Clean(self):
        for key, value in self.__tempFiles.iteritems():
            os.unlink(value)

