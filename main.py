import os
import sys

__author__ = 'Toyz'

from imvu.cfl.CFL import CFL
from imvu.chkn import ChknFile

def run(cflFile):
    cfl = CFL(cflFile)
    head, tail = os.path.split(cflFile)
    tail = tail.split(".")[0]
    tail += ".chkn"

    filename = "output/{0}".format(tail)
    make_folder(filename)
    chkn = ChknFile.ChknFile(open(filename, "wb"), "w")

    files = {}
    for name in cfl.getEntryNames():
        print "Converting: {0}".format(name)
        data = cfl.getContents(name)
        chkn.writestr(name, data)
        make_folder("output/raw/{0}".format(name))
        open("output/raw/{0}".format(name), 'wb').write(data)

    print "Saved to \'output/{0}\'".format(tail)
    chkn.close()

def make_folder(filename):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print "main.exe CFLPath"