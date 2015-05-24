__author__ = 'Toyz'

from imvu.cfl.CFL import CFL
from imvu.chkn import ChknFile

def run():
    cfl = CFL("1.cfl")
    chkn = ChknFile.ChknFile(open("output/1.chkn", "wb"), "w")

    files = {}
    for name in cfl.getEntryNames():
        print "Converting: " + name
        data = cfl.getContents(name)
        chkn.writestr(name, data)

    print "Saved to 'output/1.chkn'"
    chkn.close()

if __name__ == '__main__':
    run()