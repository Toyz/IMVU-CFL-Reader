from handlers.tools.singleton import singleton

__author__ = 'Toyz'

from handlers.cfl.CFLOpener import CFLOpener
import tempfile
import os

@singleton
class TempLoad:
    def __init__(self, cfl, default="interface"):
        if self.__doesexist(cfl):
            self.__loaded = CFLOpener(cfl)
        self.__tempFiles = {}
        self.__defaultFolder = default

    def getfile(self, cfl):
        if self.__doesexist(os.path.join(self.__defaultFolder, cfl)):
            return os.path.join(self.__defaultFolder, cfl)

        if self.__tempFiles.has_key(cfl):
            return self.__tempFiles[cfl]

        data = self.__loaded.getContents(cfl)
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(data)
        f.close()
        self.__tempFiles[cfl] = f.name
        return f.name

    def getimage(self, image, ext=".png"):
        return self.getfile(image + ext)

    def __doesexist(self, cfl):
        return os.path.isfile(cfl)

    def clean(self):
        for key, value in self.__tempFiles.iteritems():
            os.unlink(value)
