from PyQt5.QtCore import *
from PyQt5.QtGui import *

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from Data import *
from Graph import *

#
class GeneStatUI(QtWidgets.QMainWindow):
    def __init__(self):
    
        super().__init__()

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QGridLayout(self._main)

        self.ctrl = QtWidgets.QWidget()
        self.createGeneDataGroup()
        self.createProgressBar()

        clayout = QtWidgets.QGridLayout(self.ctrl)
        clayout.addWidget(self.genedataGroupBox, 0, 0)
        clayout.addWidget(self.progressBar,     1, 0)
        clayout.setRowStretch(0, 0)
        clayout.setRowStretch(1, 0)

        #layout.addWidget(self.ctrl, 0, 0, 1, 1)
        layout.addWidget(self.ctrl, 0, 0)

        ######
        # data
        self.data = GeneData(file_name='');
        self.plot = QtWidgets.QWidget()
        self.graph = GeneGraph(self.data)

        playout = QtWidgets.QGridLayout(self.plot)
        playout.addWidget(self.graph.canvas, 0, 0)
        
        self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.graph.canvas, self))
        layout.addWidget(self.plot, 0, 1, 1, 4)

        layout.setRowStretch(0, 0)
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 10)

        self.setWindowTitle("MTStatApp");

        self.setGeometry(50, 50, 1500, 1000);


    ###############################################################################
    #
    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    ###############################################################################
    #
    def clickFileNamePushButton(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open An displayMode File", "","All Files (*);;PNG Files (*.png)", options=options)
        if fileName:
            #print(fileName)
            self.fileNamelineEdit.setText(fileName)
            self.data.read_data(fileName)

            self.setupDataUIElement();
            self.updateGraph();

    ###############################################################################
    #
    def clickEnhancePushButton(self):
        if (self.data.isReady() == False):
            return;

        arg = self.enhanceEdit.text();
        self.data.enhance_image(arg);
        self.graph.showImage(1)

        self.setupDataUIElement();
        self.updateGraph();

    ###############################################################################
    #
    def clickSegmentPushButton(self):
        if (self.data.isReady() == False):
            return;

        arg = self.segmentEdit.text();
        self.data.segment_image(arg);
        self.graph.showImage(2)

        self.setupDataUIElement();
        self.updateGraph();

    ###############################################################################
    #
    def clickCalculatePushButton(self):
        if (self.data.isReady() == False):
            return;

        arg = self.calculateEdit.text();
        self.data.calculate_image();
        self.graph.showImage(3)

        self.setupDataUIElement();
        self.updateGraph();

    ###############################################################################
    #
    def onSliceChange(self):
        if (self.data.isReady() == False):
            return;
        index = self.ImageTypeSlider.value();
        if ( self.data.get_index() == index):
            return;
        self.graph.showImage(index)

    ###############################################################################
    #
    def setupDataUIElement(self):
        dim = self.data.get_dimension();

        self.ImageTypeLabel.setText("ImageType({:1d}):".format(dim[2]))

        self.ImageTypeSlider.setMinimum(0);
        self.ImageTypeSpinBox.setMinimum(0);
        self.ImageTypeSlider.setMaximum(dim[2]-1);
        self.ImageTypeSpinBox.setMaximum(dim[2]-1);

        index = self.data.get_index();
        self.ImageTypeSlider.setValue(index);

        index = self.cbDisplayMode.currentIndex()

        self.graph.setCMode(index);

        
    ###############################################################################
    #
    def updateGraph(self):

        self.graph.showImage(self.data.get_index())

    ###############################################################################
    #
    def selectionchangeDisplayModel(self, index):
        #print(index)
        self.graph.setCMode(index);

        self.updateGraph();

    ###############################################################################
    #
    def createGeneDataGroup(self):

        self.genedataGroupBox = QGroupBox("GeneData")
        self.genedataGroupBox.setCheckable(False)

        self.fileNameLabel = QLabel("GeneFileName:")
        self.fileNamelineEdit = QLineEdit('')
        self.fileNamePushButton = QPushButton("Load")
        #defaultPushButton.setDefault(True)
        self.fileNamePushButton.clicked.connect(self.clickFileNamePushButton)

        self.ImageTypeLabel = QLabel("ImageType:")
        self.ImageTypeSlider = QSlider(Qt.Horizontal, self.genedataGroupBox)
        self.ImageTypeSpinBox = QSpinBox(self.genedataGroupBox)
        self.ImageTypeSpinBox.setValue(0)
        self.ImageTypeSlider.setSingleStep(1)
        self.ImageTypeSlider.setPageStep(1)
        self.ImageTypeSlider.valueChanged[int].connect(self.ImageTypeSpinBox.setValue)
        self.ImageTypeSpinBox.valueChanged[int].connect(self.ImageTypeSlider.setValue)
        self.ImageTypeSlider.valueChanged.connect(self.onSliceChange)

        self.enhancePushButton = QPushButton("Enhance")
        self.enhancePushButton.clicked.connect(self.clickEnhancePushButton)
        self.segmentPushButton = QPushButton("Segment")
        self.segmentPushButton.clicked.connect(self.clickSegmentPushButton)
        self.calculatePushButton = QPushButton("Calculate")
        self.calculatePushButton.clicked.connect(self.clickCalculatePushButton)

        self.enhanceEdit = QLineEdit("")
        self.segmentEdit = QLineEdit("")
        self.calculateEdit = QLineEdit("")

        self.displayModeLabel = QLabel("DisplayMode:");
        self.cbDisplayMode = QComboBox()
        self.cbDisplayMode.addItem("Raw image")
        self.cbDisplayMode.addItem("x over 0")
        self.cbDisplayMode.addItem("x over 1")
        self.cbDisplayMode.addItem("x over 2")
        self.cbDisplayMode.currentIndexChanged.connect(self.selectionchangeDisplayModel)

        self.infoEdit = QTextEdit()
        self.infoEdit.setPlainText("...")


        layout = QGridLayout()
        layout.addWidget(self.fileNameLabel,            0, 0, 1, 1)
        layout.addWidget(self.fileNamelineEdit,         0, 1, 1, 8)
        layout.addWidget(self.fileNamePushButton,       0, 9, 1, 1)

        layout.addWidget(self.ImageTypeLabel,           1, 0, 1, 1)
        layout.addWidget(self.ImageTypeSlider,          1, 1, 1, 8)
        layout.addWidget(self.ImageTypeSpinBox,         1, 9, 1, 1)

        layout.addWidget(self.enhancePushButton,        2, 0, 1, 5)
        layout.addWidget(self.enhanceEdit,              2, 5, 1, 5)

        layout.addWidget(self.segmentPushButton,        3, 0, 1, 5)
        layout.addWidget(self.segmentEdit,              3, 5, 1, 5)

        layout.addWidget(self.calculatePushButton,      4, 0, 1, 5)
        layout.addWidget(self.calculateEdit,            4, 5, 1, 5)

        layout.addWidget(self.displayModeLabel,         5, 0, 1, 1)
        layout.addWidget(self.cbDisplayMode,            5, 1, 1, 1)


        layout.addWidget(self.infoEdit,                 6, 0, 4, 10)

        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 0)
        layout.setRowStretch(2, 0)
        layout.setRowStretch(3, 0)
        layout.setRowStretch(9, 10)

        #layout.setColumnStretch(1, 1)
        self.genedataGroupBox.setLayout(layout)

    ###############################################################################
    #
    def createProgressBar(self):

        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        #timer = QTimer(self)
        #timer.timeout.connect(self.advanceProgressBar)
        #timer.start(1000)
#class end 
###############################################################################
