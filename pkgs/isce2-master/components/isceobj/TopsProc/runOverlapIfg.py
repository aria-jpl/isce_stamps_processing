#
# Author: Piyush Agram
# Copyright 2016
#


import isceobj
import stdproc
from stdproc.stdproc import crossmul
import numpy as np
from isceobj.Util.Poly2D import Poly2D
import argparse
import os
import copy
from isceobj.Sensor.TOPS import createTOPSSwathSLCProduct
from .runBurstIfg import adjustValidLineSample


def takeLooks(inimg, alks, rlks):
    '''
    Take looks.
    '''

    from mroipac.looks.Looks import Looks

    spl = os.path.splitext(inimg.filename)
    ext = '.{0}alks_{1}rlks'.format(alks, rlks)
    outfile = spl[0] + ext + spl[1]


    lkObj = Looks()
    lkObj.setDownLooks(alks)
    lkObj.setAcrossLooks(rlks)
    lkObj.setInputImage(inimg)
    lkObj.setOutputFilename(outfile)
    lkObj.looks()

    return outfile

def loadVirtualArray(fname):
    from osgeo import gdal

    ds = gdal.Open(fname, gdal.GA_ReadOnly)
    data = ds.GetRasterBand(1).ReadAsArray()

    ds = None
    return data

def multiply(masname, slvname, outname, rngname, fact, masterFrame,
        flatten=True, alks=3, rlks=7, virtual=True):


    masImg = isceobj.createSlcImage()
    masImg.load( masname + '.xml')

    width = masImg.getWidth()
    length = masImg.getLength()


    if not virtual:
        master = np.memmap(masname, dtype=np.complex64, mode='r', shape=(length,width))
        slave = np.memmap(slvname, dtype=np.complex64, mode='r', shape=(length, width))
    else:
        master = loadVirtualArray(masname + '.vrt')
        slave = loadVirtualArray(slvname + '.vrt')
   
    if os.path.exists(rngname):
        rng2 = np.memmap(rngname, dtype=np.float32, mode='r', shape=(length,width))
    else:
        print('No range offsets provided')
        rng2 = np.zeros((length,width))

    cJ = np.complex64(-1j)
    
    #Zero out anytging outside the valid region:
    ifg = np.memmap(outname, dtype=np.complex64, mode='w+', shape=(length,width))
    firstS = masterFrame.firstValidSample
    lastS = masterFrame.firstValidSample + masterFrame.numValidSamples -1
    firstL = masterFrame.firstValidLine
    lastL = masterFrame.firstValidLine + masterFrame.numValidLines - 1
    for kk in range(firstL,lastL + 1):
        ifg[kk,firstS:lastS + 1] = master[kk,firstS:lastS + 1] * np.conj(slave[kk,firstS:lastS + 1])
        if flatten:
            phs = np.exp(cJ*fact*rng2[kk,firstS:lastS + 1])
            ifg[kk,firstS:lastS + 1] *= phs

    ####
    master=None
    slave=None
    ifg = None

    objInt = isceobj.createIntImage()
    objInt.setFilename(outname)
    objInt.setWidth(width)
    objInt.setLength(length)
    objInt.setAccessMode('READ')
    objInt.renderHdr()

    try:
        outfile = takeLooks(objInt, alks, rlks)
        print('Output: ', outfile)
    except:
        raise Exception('Failed to multilook ifgs')

    return objInt


def runOverlapIfg(self):
    '''Create overlap interferograms.
    '''

    virtual = self.useVirtualFiles
    if not self.doESD:
        return 


    swathList = self._insar.getValidSwathList(self.swaths)

    for swath in swathList:

        if self._insar.numberOfCommonBursts[swath-1] < 2:
            print('Skipping overlap ifg for swath IW{0}'.format(swath))
            continue

        minBurst = self._insar.commonBurstStartMasterIndex[swath-1]
        maxBurst = minBurst + self._insar.numberOfCommonBursts[swath-1]

        nBurst = maxBurst - minBurst

        ifgdir = os.path.join( self._insar.coarseIfgDirname, self._insar.overlapsSubDirname, 'IW{0}'.format(swath))
        if not os.path.exists(ifgdir):
            os.makedirs(ifgdir)

        ####All indexing is w.r.t stack master for overlaps
        maxBurst = maxBurst - 1
   

        ####Load relevant products
        topMaster = self._insar.loadProduct(os.path.join(self._insar.masterSlcOverlapProduct, 'top_IW{0}.xml'.format(swath)))
        botMaster = self._insar.loadProduct(os.path.join(self._insar.masterSlcOverlapProduct, 'bottom_IW{0}.xml'.format(swath)))

        topCoreg = self._insar.loadProduct( os.path.join(self._insar.coregOverlapProduct,'top_IW{0}.xml'.format(swath)))
        botCoreg = self._insar.loadProduct( os.path.join(self._insar.coregOverlapProduct, 'bottom_IW{0}.xml'.format(swath)))

        coregdir = os.path.join(self._insar.coarseOffsetsDirname, self._insar.overlapsSubDirname, 'IW{0}'.format(swath))

        topIfg = createTOPSSwathSLCProduct()
        topIfg.configure()

        botIfg = createTOPSSwathSLCProduct()
        botIfg.configure()

        for ii in range(minBurst, maxBurst):
    
            jj = ii - minBurst

            ####Process the top bursts
            master = topMaster.bursts[jj] 
            slave  = topCoreg.bursts[jj]

            mastername = master.image.filename
            slavename = slave.image.filename
            rdict = {'rangeOff' : os.path.join(coregdir, 'range_top_%02d_%02d.off'%(ii+1,ii+2)),
                     'azimuthOff': os.path.join(coregdir, 'azimuth_top_%02d_%02d.off'%(ii+1,ii+2))}
            
            
            adjustValidLineSample(master,slave)
        
            intname = os.path.join(ifgdir, '%s_top_%02d_%02d.int'%('burst',ii+1,ii+2))
            fact = 4 * np.pi * slave.rangePixelSize / slave.radarWavelength
            intimage = multiply(mastername, slavename, intname,
                        rdict['rangeOff'], fact, master, flatten=True,
                        alks = self.numberAzimuthLooks, rlks=self.numberRangeLooks)

            burst = master.clone()
            burst.image = intimage
            topIfg.bursts.append(burst)



            ####Process the bottom bursts
            master = botMaster.bursts[jj]
            slave = botCoreg.bursts[jj]


            mastername =  master.image.filename
            slavename = slave.image.filename
            rdict = {'rangeOff' : os.path.join(coregdir, 'range_bot_%02d_%02d.off'%(ii+1,ii+2)),
                    'azimuthOff': os.path.join(coregdir, 'azimuth_bot_%02d_%02d.off'%(ii+1,ii+2))}

            adjustValidLineSample(master,slave)
            intname = os.path.join(ifgdir, '%s_bot_%02d_%02d.int'%('burst',ii+1,ii+2))
            fact = 4 * np.pi * slave.rangePixelSize / slave.radarWavelength
            intimage = multiply(mastername, slavename, intname,
                        rdict['rangeOff'], fact, master, flatten=True,
                        alks = self.numberAzimuthLooks, rlks=self.numberRangeLooks,
                        virtual=virtual)

            burst = master.clone()
            burst.image = intimage
            botIfg.bursts.append(burst)


        topIfg.numberOfBursts = len(topIfg.bursts)
        botIfg.numberOfBursts = len(botIfg.bursts)

        self._insar.saveProduct(topIfg, os.path.join(self._insar.coarseIfgOverlapProduct, 'top_IW{0}.xml'.format(swath)))
        self._insar.saveProduct(botIfg, os.path.join(self._insar.coarseIfgOverlapProduct, 'bottom_IW{0}.xml'.format(swath)))
