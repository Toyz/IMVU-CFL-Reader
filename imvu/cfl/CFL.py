__author__ = 'Toyz'


import struct
import pylzma
import contextlib
import imvu.cfl
CFLCOMPRESS_NONE = 0
CFLCOMPRESS_LZMA = 4

class InvalidCFLError(Exception):
    pass


def decompress(flag, compressed):
    if flag == CFLCOMPRESS_NONE:
        return compressed
    if flag == CFLCOMPRESS_LZMA:
        try:
            return pylzma.decompress(compressed)
        except (TypeError, ValueError) as e:
            raise InvalidCFLError(e)

    else:
        raise InvalidCFLError('Unsupported flag %r' % (flag,))


def readInt(f):
    try:
        return struct.unpack('<I', f.read(4))[0]
    except struct.error:
        raise InvalidCFLError


def loadResource(f):
    compressedSize = readInt(f)
    return f.read(compressedSize)


class CFL(object):

    def __init__(self, path):
        self.__path = path
        with self.__openCFL() as f:
            header = f.read(4)
            if header not in ('CFL3', 'DFL3'):
                raise InvalidCFLError(path)
            supportsContentHash = header == 'DFL3'
            f.seek(readInt(f))
            directoryCompression = readInt(f)
            directory = decompress(directoryCompression, loadResource(f))
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
            raise imvu.cfl.CflMissingAssetsError(entryName)

        with self.__openCFL() as f:
            f.seek(entry['offset'])
            return decompress(entry['compression'], loadResource(f))

    def getFileSize(self, entryName):
        return self.__entries[entryName]['fileSize']

    def getCompressedFileSize(self, entryName):
        entry = self.__entries[entryName]
        with self.__openCFL() as f:
            f.seek(entry['offset'])
            return readInt(f)

    @contextlib.contextmanager
    def __openCFL(self):
        f = open(self.__path, "rb")
        yield f
        f.close()
