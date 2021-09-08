from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from Data import *
from MTStatUI import *

###############################################################################
#
class GeneGraph(object):
    def __init__(self, data, cmode=0):
    
        self.data = data;
        self.mode = 0; # zslice only
        self.cmode = cmode; # channel mode

        self.canvas = FigureCanvas(Figure(figsize=(4, 4)))
        #self.ax = self.canvas.figure.subplots(2,2)

        self.ax = self.canvas.figure.subplots()

        #self.ax[0,0].clear()
        #t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        #self.ax[0,0].plot(t, np.sin(t + time.time()))
        #self.ax[0,0].figure.canvas.draw()

    ###############################################################################
    #
    def setCMode(self, md):
        self.cmode = md;

    #
    def setMode(self, md):
        self.mode = md;

    ###############################################################################
    #
    def showImage(self, index):
        if (self.data.isReady() == False):
            return;

        self.data.set_index(index)
        if (self.cmode == 0):
            img = self.data.get_image(self.data.get_index());
        elif (self.cmode == 1):
            img = self.data.get_image_c(self.data.get_index(), self.cmode);
        elif (self.cmode == 2):
            img = self.data.get_image_c(self.data.get_index(), self.cmode);
        else:
            img = self.data.get_image_c(self.data.get_index(), self.cmode);

        self.ax.imshow(img)
        self.ax.figure.canvas.draw()

    ###############################################################################
    # Do a mouseclick somewhere, move the mouse to some destination, release
    # the button.  This class gives click- and release-events and also draws
    # a line or a box from the click-point to the actual mouseposition
    # (within the same axes) until the button is released.  Within the
    # method 'self.ignore()' it is checked whether the button from eventpress
    # and eventrelease are the same.

    def line_select_callback(eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        print(" The button you used were: %s %s" % (eclick.button, erelease.button))


    def toggle_selector(event):
        print(' Key pressed.')
        if event.key in ['Q', 'q'] and toggle_selector.RS.active:
            print(' RectangleSelector deactivated.')
            toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not toggle_selector.RS.active:
            print(' RectangleSelector activated.')
            toggle_selector.RS.set_active(True)

    def setupROISelection(self):
        # drawtype is 'box' or 'line' or 'none'
        self.toggle_selector.RS = RectangleSelector(current_ax, line_select_callback,
                                               drawtype='box', useblit=True,
                                               button=[1, 3],  # don't use middle button
                                               minspanx=5, minspany=5,
                                               spancoords='pixels',
                                               interactive=True)
        plt.connect('key_press_event', toggle_selector)
    ###############################################################################
    #

#class end 
###############################################################################
