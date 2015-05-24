__author__ = 'Toyz'

import zipfile

class ChknFile(zipfile.ZipFile):

    def __init__(self, file, mode, compress = True):
        cmode = zipfile.ZIP_DEFLATED
        if not compress:
            cmode = zipfile.ZIP_STORED
        return zipfile.ZipFile.__init__(self, file, mode, cmode, False)
