__author__ = 'Toyz'

from handlers.cfl.CFL import CFL
import tempfile
import os
class TempLoad:
    def __init__(self, cfl, default="interface"):
        if self.__doesEixst(cfl):
            self.__loaded = CFL(cfl)
        self.__tempFiles = {}
        self.__defaultFolder = default

    def GetFile(self, cfl):
        if self.__doesEixst(os.path.join(self.__defaultFolder, cfl)):
            return os.path.join(self.__defaultFolder, cfl)

        if self.__tempFiles.has_key(cfl):
            return self.__tempFiles[cfl]

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

