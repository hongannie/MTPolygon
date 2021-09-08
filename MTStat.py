import os, time, pickle, argparse
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from PyQt5.QtWidgets import (QApplication)
from MTStatUI import *

###############################################################################
###############################################################################
def parseArg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',     required=False,             default="",     help='file name')
    parser.add_argument('--verbose',  required=False,             default=1,      help='verbose level')
 
    opt = parser.parse_args()

    print(opt)

    return opt


def doUI(opt):

    import sys
    qapp = QtWidgets.QApplication(sys.argv)
    gsui = GeneStatUI()
    gsui.show()
    sys.exit(qapp.exec_()) 

###############################################################################
###############################################################################
if __name__ == '__main__':

    opt = parseArg()

    doUI(opt)
