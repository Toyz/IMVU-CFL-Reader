from handlers.tools import Utils

__author__ = 'Toyz'

import struct


class CFLMaker(object):

    def __init__(self, path):
        self.__path = path
        self.__entries = {}
        self.__file = open(self.__path, 'wb')
        self.__file.write('CFL3')
        self.__writeInt(0)
        self.__writeInt(0)
        self.__curOffset = self.__file.tell()

    def path(self):
        return self.__path

    def store(self, entryName, entryData):
        unicode(entryName)
        cdata = Utils.Utils.compress(Utils.CFLCOMPRESS_LZMA, entryData)
        self.__writeInt(len(cdata))
        self.__file.write(cdata)
        self.__entries[entryName] = dict(offset=self.__curOffset, compression=Utils.CFLCOMPRESS_LZMA, fileSize=len(entryData))
        self.__curOffset = self.__file.tell()

    def finish(self):
        entryDatas = []
        for name, info in self.__entries.items():
            entryData = struct.pack('<iiih', info['fileSize'], info['offset'], info['compression'], len(name))
            entryData += name.encode('latin-1')
            entryDatas.append(entryData)

        directoryData = ''.join(entryDatas)
        dirSize = len(directoryData)
        directoryCompression = Utils.CFLCOMPRESS_LZMA
        cdata = Utils.Utils.compress(directoryCompression, directoryData)
        dirOffset = self.__file.tell()
        self.__writeInt(directoryCompression)
        self.__writeInt(len(cdata))
        self.__file.write(cdata)
        self.__file.seek(4)
        self.__writeInt(dirOffset)
        self.__writeInt(dirSize)
        self.__file.close()
        self.__file = None
        return

    def __writeInt(self, v):
        return self.__file.write(struct.pack('<I', v))
