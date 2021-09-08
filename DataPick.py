import numpy as np
import re
import cv2
import os, time, pickle, argparse
import datetime
from skimage import data
from skimage import color
from skimage import measure
from skimage.filters import meijering, sato, frangi, hessian, threshold_niblack, threshold_sauvola, gaussian 
from skimage.morphology import remove_small_objects, remove_small_holes, skeletonize, binary_dilation, binary_erosion
from skimage.measure import label, regionprops
from skimage.color import label2rgb
#import xlwt 



import matplotlib.pyplot as plt
#from xlwt import Workbook

#set a backend for matplotlib
import matplotlib
from PIL import Image
from pylab import *
matplotlib.use('TkAgg')


class GeneData(object):

    def __init__(self, file_name='', xscale=1, yscale=1, zscale=1, parent=None):
    
        self.data_file = file_name;

        self.ready = False;
        self.readyEnhance = False;
        self.readySegment = False;
        self.readyCalculate = False;
        self.readyPickNucleus = False;

        self.imageRaw = 0;
        self.imageSmooth = 1;
        self.imageTubeness = 2;
        self.imageBinary = 3;
        self.imageBinaryClean = 4;
        self.imageBinaryClosing = 5;
        self.imageBinaryCleanHole = 6;
        self.imageThin = 7;
        self.imageLabel = 8;
        
        self.xNucleus = 0;
        self.yNucleus = 0;

        self.initialize();

    ###############################################################################
    #
    def initialize(self):
    
        self.ready = False;

        self.data_raw = np.zeros(shape=(0,0,0), dtype='uint32');
        self.data_3d = np.zeros(shape=(0,0,0), dtype='uint8');

        self.index=0;

        if (self.data_file != ''):
            self.read_image(file_name=self.data_file);

    ###############################################################################
    #
    def read_data( self, file_name=''):
        self.data_file = file_name;
        self.initialize();

    ###############################################################################
    #
    def isReady( self):
        return self.ready;

    ###############################################################################
    #
    def set_index(self, index):
        self.index = max(0, min(self.data_3d.shape[2]-1,index));

    ###############################################################################
    #
    def get_index(self):
        return self.index;

    ###############################################################################
    #
    def get_dimension( self):
        dim = np.zeros(shape=(3), dtype='uint32')
        dim[0] = self.data_3d.shape[0];
        dim[1] = self.data_3d.shape[1];
        dim[2] = self.data_3d.shape[2];
        return dim;

    ###############################################################################
    #
    def get_image ( self, index ):
        index = min(index, self.data_3d.shape[2]-1)
        index = max(index, 0)
        img = np.reshape(self.data_3d[:, :, index], newshape=(self.data_3d.shape[0], self.data_3d.shape[1])) ;

        return img

    def set_image ( self, index, img ):
        index = min(index, self.data_3d.shape[2]-1)
        index = max(index, 0)
        self.data_3d[:, :, index] = img

    def get_image_c ( self, index, cindex ):
        index = min(index, self.data_3d.shape[2]-1)
        index = max(index, 0)

        img = np.zeros(shape=(self.data_raw.shape[0], self.data_raw.shape[1], 3), dtype='uint32')

        if (cindex >= 1) and (index == self.imageLabel):
            img = label2rgb(self.data_3d[:, :, index], image=self.data_3d[:, :, 0])
        elif (cindex == 1) and (index >= 3):
            img[:, :, 0] = self.data_3d[:, :, 0]
            img[:, :, 1] = self.data_3d[:, :, 0]
            img[:, :, 2] = self.data_3d[:, :, 0]
            msk = np.zeros(shape=(self.data_raw.shape[0], self.data_raw.shape[1]), dtype='uint8')
            msk[self.data_3d[:, :, index] > 0] = 128;
            simg = img[:, :, 0];
            simg[msk > 0] = 255
            img[:, :, 0] = simg;
            #
            simg = img[:, :, 1];
            simg[msk > 0] = 0
            img[:, :, 1] = simg;
            #
            simg = img[:, :, 2];
            simg[msk > 0] = 0
            img[:, :, 2] = simg;
        elif (cindex == 2) and  (index >= 3):
            img[:, :, 0] = self.data_3d[:, :, 1]
            img[:, :, 1] = self.data_3d[:, :, 1]
            img[:, :, 2] = self.data_3d[:, :, 1]
            msk = np.zeros(shape=(self.data_raw.shape[0], self.data_raw.shape[1]), dtype='uint8')
            msk[self.data_3d[:, :, index] > 0] = 128;
            simg = img[:, :, 0];
            simg[msk > 0] = 255
            img[:, :, 0] = simg;
            #
            simg = img[:, :, 1];
            simg[msk > 0] = 0
            img[:, :, 1] = simg;
            #
            simg = img[:, :, 2];
            simg[msk > 0] = 0
            img[:, :, 2] = simg;
        elif (cindex == 3) and  (index >= 3):
            img[:, :, 0] = self.data_3d[:, :, 2]
            img[:, :, 1] = self.data_3d[:, :, 2]
            img[:, :, 2] = self.data_3d[:, :, 2]
            msk = np.zeros(shape=(self.data_raw.shape[0], self.data_raw.shape[1]), dtype='uint8')
            msk[self.data_3d[:, :, index] > 0] = 128;
            simg = img[:, :, 0];
            simg[msk > 0] = 255
            img[:, :, 0] = simg;
            #
            simg = img[:, :, 1];
            simg[msk > 0] = 0
            img[:, :, 1] = simg;
            #
            simg = img[:, :, 2];
            simg[msk > 0] = 0
            img[:, :, 2] = simg;
        
        else:
            img = np.reshape(self.data_3d[:, :, index], newshape=(self.data_3d.shape[0], self.data_3d.shape[1])) ;

        return img

    ###############################################################################
    def read_image ( self, file_name='' ):

        img = cv2.imread(file_name)

        self.data_raw = img;

        dx = self.data_raw.shape[0];
        dy = self.data_raw.shape[1];
        dz = 10;

        if (img.ndim > 2):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img;

        self.data_3d = np.zeros(shape=(dx, dy, dz), dtype='uint8')

        gray = cv2.resize(gray, dsize=(dy, dx), interpolation=cv2.INTER_LINEAR)

        gray = np.reshape(gray, newshape=(self.data_3d.shape[0], self.data_3d.shape[1])) ;

        self.set_image ( self.imageRaw, gray );

        self.ready = True;
        self.readyEnhance = False;
        self.readySegment = False;
        self.readyCalculate = False;
        self.readyPickNucleus = False;

    #def read_image

    ###############################################################################
    def getAFloatParameter ( self, prefixstr, arg="", defval=0 ):
        value = defval;
        prefix = re.search(prefixstr, arg)
        if (prefix != None):
            val = re.search("[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?", arg[prefix.end():])
            if (val != None):
                value = float(arg[prefix.end()+val.start():prefix.end()+val.end()]);
        return value

    ###############################################################################
    def enhance_image ( self, arg="" ):

        if (self.ready != True):
            return;

        img = self.get_image (0)

        # smooth
        smooth_sigma = self.getAFloatParameter ( "smooth_sigma=", arg, defval=1 )
        print ( "smooth_sigma = ", smooth_sigma)
        rimg = gaussian(img, sigma=smooth_sigma)
        self.set_image(self.imageSmooth, rimg);

        tubenessAlgorithm = self.getAFloatParameter ( "tubenessalgorithm=", arg, defval=0)
        print ( "tubenessAlgorithm = ", tubenessAlgorithm)
        #
        tubenessLow = 3;
        tubenessHigh = 10;
        rangelow = self.getAFloatParameter ( "rangelow=", arg, defval=tubenessLow )
        print ( "rangelow = ", rangelow)
        rangehigh = self.getAFloatParameter ( "rangehigh", arg, defval=tubenessHigh )
        print ( "rangehigh = ", rangehigh)

        if (tubenessAlgorithm == 0):
            print ("meijering")
            result = meijering(rimg, sigmas=range(rangelow,rangehigh,1), black_ridges=False)
            result = result * 255;
        elif (tubenessAlgorithm == 1):
            print ("frangi")
            result = frangi(rimg, sigmas=range(rangelow,rangehigh,1), black_ridges=False)
            result = result * 255;
        elif (tubenessAlgorithm == 2):
            print ("hessian")
            result = hessian(rimg, sigmas=range(rangelow,rangehigh,1), black_ridges=False)
            result = result * 255;
        else:
            print ("sato")
            result = sato(rimg, sigmas=range(rangelow,rangehigh,1), black_ridges=False)
            result = result * 255;

        self.set_image(self.imageTubeness, result);

        self.readyEnhance = True;

    #def

    ###############################################################################
    def segment_image ( self, arg="" ):

        if (self.readyEnhance != True):
            self.enhance_image ();
        if (self.readyEnhance != True):
            return;

        use = self.getAFloatParameter ( "use=", arg, defval=1 )
        print ("use = ", use)
        #
        if (use == 1):
            img = self.get_image (self.imageTubeness)
        elif (use == 2):
            img = self.get_image (self.imageSmooth)
        else:
            img = self.get_image (self.imageRaw)

        # binarize
        binaryAlgorithm = 0;
        binaryAlgorithm = self.getAFloatParameter ( "k=", arg, defval=0 )
        print ("binaryAlgorithm = ", binaryAlgorithm)
        window_size = self.getAFloatParameter ( "window_size=", arg, defval=25 )
        print ("window_size = ", window_size)
        if (binaryAlgorithm==0):
            print ("binaryAlgorithm = threshold_sauvola")
            k = self.getAFloatParameter ( "k=", arg, defval=0.2 )
            print ("k = ", k)
            threshold_image = threshold_sauvola(img, window_size=window_size, k=k)
        else:
            print ("binaryAlgorithm = niblack")
            k = self.getAFloatParameter ( "k=", arg, defval=-0.25 )
            print ("k = ", k)
            threshold_image = threshold_niblack(img, window_size=window_size, k=k)
        resultbinary = img > threshold_image;
        self.set_image( self.imageBinary, resultbinary );

        # clean
        min_size = self.getAFloatParameter ( "min_size", arg, defval=200 )
        print ( "min_size = ", min_size)
        resultsmall = remove_small_objects (resultbinary, min_size=min_size );
        self.set_image ( self.imageBinaryClean, resultsmall );

        # closing
        closing_size = self.getAFloatParameter ( "closing_size", arg, defval=5 )
        print ( "closing_size = ", closing_size)
        resultclosing = resultsmall
        for i in range(closing_size):
            resultclosing = binary_dilation (resultclosing );
        for i in range(closing_size):
            resultclosing = binary_erosion (resultclosing );
        self.set_image ( self.imageBinaryClosing, resultclosing );

        # fill hole
        area_threshold = self.getAFloatParameter ( "area_threshold", arg, defval=10 )
        print ( "area_threshold = ", area_threshold)
        resulthole = remove_small_holes (resultclosing, area_threshold=area_threshold );
        self.set_image ( self.imageBinaryCleanHole, resulthole );

        # thinning
        resultthin = skeletonize ( resulthole )
        resultthin = binary_dilation ( resultthin );
        self.set_image ( self.imageThin, resultthin )

        # clean up

        self.readySegment = True;

    #def

    ###############################################################################
    def calculate_image ( self, arg="" ):

        if (self.readySegment != True):
            self.segment_image ();
        if (self.readySegment != True):
            return;

        use = self.getAFloatParameter ( "use=", arg, defval=1 )
        print ("use = ", use)
        
        img = self.get_image (self.imageThin)
        img = img == 0

        # label
        label_image = label(img, background=-1)
        

        self.set_image ( self.imageLabel, label_image )
        
        #get areas and centroid and write to file
        props = measure.regionprops(label_image)
        file = open("testing.txt", "w")
        for prop in props:
           #file.write('{} {}\n'.format(prop.area, prop.centroid))
           file.write('{} \n'.format(prop.area))
        file.close()
    

        self.readyCalculate = True;
    ###############################################################################
    def pick_nucleus ( self, arg="" ):

        #get the location of the nucleus by clicking and save to file
        im = array(Image.open('microbes2.jpg'))
        imshow(im)
        k = waitKey(1)
        nucleus = ginput(1)
        print ("nucleus = ", nucleus)
        file = open("nucleus_location.txt", "w")
        file.write('{} \n'.format(nucleus))
        file.close()
        k = waitKey(1)
        destroyAllWindows()
    
        self.readyPickNucleus = True;

    #def
