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
        """Return a nicely shortened string if over a set upper limit
        (default 75 characters)

        What is nicely shortened? Consider this line from Orwell's 1984...
        0---------1---------2---------3---------4---------5---------6---------7---->
        When we are omnipotent we shall have no more need of science. There will be

        If the limit is set to 70, a hard truncation would result in...
        When we are omnipotent we shall have no more need of science. There wi...

        Truncating to the nearest space might be better...
        When we are omnipotent we shall have no more need of science. There...

        The best truncation would be...
        When we are omnipotent we shall have no more need of science...

        Therefore, the returned string will be, in priority...

        1. If the string is less than the limit, just return the whole string
        2. If the string has a period, return the string from zero to the first
            period from the right
        3. If the string has no period, return the string from zero to the first
            space
        4. If there is no space or period in the range return a hard truncation

        In all cases, the string returned will have ellipsis appended unless
        otherwise specified.

        Parameters:
            s = string to be truncated as a String
            min_pos = minimum character index to return as Integer (returned
                      string will be at least this long - default 0)
            max_pos = maximum character index to return as Integer (returned
                      string will be at most this long - default 75)
            ellipsis = returned string will have an ellipsis appended to it
                       before it is returned if this is set as Boolean
                       (default is True)
        Returns:
            Truncated String
        Throws:
            ValueError exception if min_pos > max_pos, indicating improper
            configuration
        Usage:
        short_string = trunc(some_long_string)
        or
        shorter_string = trunc(some_long_string,max_pos=15,ellipsis=False)
        """
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
