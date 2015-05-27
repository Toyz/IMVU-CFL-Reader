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
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
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
    def trunc(s, min_pos=0, max_pos=75, ellipsis=True):
        # Sentinel value -1 returned by String function rfind
        NOT_FOUND = -1
        # Error message for max smaller than min positional error
        ERR_MAXMIN = 'Minimum position cannot be greater than maximum position'

        # If the minimum position value is greater than max, throw an exception
        if max_pos < min_pos:
            raise ValueError(ERR_MAXMIN)
        # Change the ellipsis characters here if you want a true ellipsis
        if ellipsis:
            suffix = '...'
        else:
            suffix = ''
        # Case 1: Return string if it is shorter (or equal to) than the limit
        length = len(s)
        if length <= max_pos:
            return s + suffix
        else:
            # Case 2: Return it to nearest period if possible
            try:
                end = s.rindex('.', min_pos, max_pos)
            except ValueError:
                # Case 3: Return string to nearest space
                end = s.rfind(' ', min_pos, max_pos)
                if end == NOT_FOUND:
                    end = max_pos
            return s[0:end] + suffix

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
