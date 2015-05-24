import os
import sys
from Tools.Utils import Utils

__author__ = 'Toyz'

from imvu.cfl.CFL import CFL
from imvu.chkn import ChknFile

def run(cflfile):
    cfl = CFL(cflfile)
    head, tail = os.path.split(cflfile)
    tail = tail.split(".")[0]
    tail += ".chkn"

    filename = "output/{0}".format(tail)
    Utils.make_folder(filename)
    chkn = ChknFile.ChknFile(open(filename, "wb"), "w")

    files = {}
    for name in cfl.getEntryNames():
        print "Converting: {0}".format(name)
        data = cfl.getContents(name)
        chkn.writestr(name, data)
        Utils.make_folder("output/raw/{0}".format(name))
        open("output/raw/{0}".format(name), 'wb').write(data)

    print "Saved to \'output/{0}\'".format(tail)
    chkn.close()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print "main.exe CFLPath"

raw_input()
