__author__ = 'Toyz'

from imvu.cfl import CFL, CFLMaker
from imvu.chkn import ChknFile

def run():
    cfl = CFL.CFL("1.cfl")
    chkn = ChknFile.ChknFile(open("output/1.chkn", "wb"), "w")

    files = {}
    for name in cfl.getEntryNames():
        print "Converting: " + name
        data = cfl.getContents(name)
        chkn.writestr(name, data)

    chkn.close()

if __name__ == '__main__':
    run()