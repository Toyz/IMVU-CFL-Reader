__author__ = 'Toyz'

import struct
import contextlib

import handlers.cfl
from handlers.tools.Utils import InvalidCFLError
from handlers.tools import Utils


def loadResource(f):
    compressedSize = Utils.Utils.readInt(f)
    return f.read(compressedSize)

class CFLOpener(object):

    def __init__(self, path):
        self.__path = path
        with self.__openCFL() as f:
            header = f.read(4)
            if header not in ('CFL3', 'DFL3'):
                raise InvalidCFLError(path)
            supportsContentHash = header == 'DFL3'
            f.seek(Utils.Utils.readInt(f))
            directoryCompression = Utils.Utils.readInt(f)
            directory = Utils.Utils.decompress(directoryCompression, loadResource(f))
            self.files = []
            self.__entries = {}
            while directory:
                entryHeader = directory[:14]
                unpackedSize, offset, compression, namelen = struct.unpack('<iiih', entryHeader)
                entryName = directory[14:14 + namelen].decode('latin-1')
                directory = directory[14 + namelen:]
                if supportsContentHash:
                    contentHashLength, = struct.unpack('<i', directory[:4])
                    contentHash = directory[4:4 + contentHashLength]
                    directory = directory[4 + contentHashLength:]
                self.files.append(entryName)
                self.__entries[entryName] = {'offset': offset,
                 'compression': compression,
                 'fileSize': unpackedSize}

    def getEntryNames(self):
        return self.__entries.keys()

    def getContents(self, entryName):
        unicode(entryName)
        try:
            entry = self.__entries[entryName]
        except KeyError:
            raise handlers.cfl.CflMissingAssetsError(entryName)

        with self.__openCFL() as f:
            f.seek(entry['offset'])
            return Utils.Utils.decompress(entry['compression'], loadResource(f))

    def getFileSize(self, entryName):
        return self.__entries[entryName]['fileSize']

    def getCompressedFileSize(self, entryName):
        entry = self.__entries[entryName]
        with self.__openCFL() as f:
            f.seek(entry['offset'])
            return Utils.Utils.readInt(f)

    @contextlib.contextmanager
    def __openCFL(self):
        f = open(self.__path, "rb")
        yield f
        f.close()
