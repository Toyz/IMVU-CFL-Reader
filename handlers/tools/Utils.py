__author__ = 'Toyz'

import struct
import pylzma


class InvalidCFLError(Exception):
    pass


CFLCOMPRESS_NONE = 0
CFLCOMPRESS_LZMA = 4


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def readInt(f):
        try:
            return struct.unpack('<I', f.read(4))[0]
        except struct.error:
            raise InvalidCFLError

    @staticmethod
    def sizeof_fmt(num, suffix='B'):
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "%3.1f %s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f %s%s" % (num, 'Yi', suffix)

    @staticmethod
    def compress(flag, plaintext):
        if flag == CFLCOMPRESS_NONE:
            return plaintext
        if flag == CFLCOMPRESS_LZMA:
            return pylzma.compress(plaintext)
        raise NotImplementedError('Unsupported flag %r' % (flag,))

    @staticmethod
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

    @staticmethod
    def make_folder(filename):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))