#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright 2012 California Institute of Technology. ALL RIGHTS RESERVED.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# United States Government Sponsorship acknowledged. This software is subject to
# U.S. export control laws and regulations and has been classified as 'EAR99 NLR'
# (No [Export] License Required except when exporting to an embargoed country,
# end user, or in support of a prohibited end use). By downloading this software,
# the user agrees to comply with all applicable U.S. export laws and regulations.
# The user has the responsibility to obtain export licenses, or other export
# authority as may be required before exporting this software to any 'EAR99'
# embargoed foreign country or citizen of those countries.
#
# Author: Brett George
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import logging
import stdproc
from stdproc.rectify.geocode.Geocodable import Geocodable
import isceobj
import iscesys
from iscesys.ImageUtil.ImageUtil import ImageUtil as IU
from iscesys.StdOEL.StdOELPy import create_writer
import os

logger = logging.getLogger('isce.insar.runGeocode')
posIndx = 1

def runGeocode(self, prodlist, unwrapflag, bbox):
    '''Generalized geocoding of all the files listed above.'''
    from isceobj.Catalog import recordInputsAndOutputs
    logger.info("Geocoding Image")
    insar = self.insar

    if isinstance(prodlist,str):
        from isceobj.Util.StringUtils import StringUtils as SU
        tobeGeocoded = SU.listify(prodlist)
    else:
        tobeGeocoded = prodlist

    #remove files that have not been processed
    for toGeo in tobeGeocoded:
        if not os.path.exists(toGeo):
            tobeGeocoded.remove(toGeo)
    print('Number of products to geocode: ', len(tobeGeocoded))

    stdWriter = create_writer("log", "", True, filename="geo.log")

    v,h = insar.vh()
    planet = insar.masterFrame._instrument._platform._planet


    if bbox is None:
        snwe = insar.topo.snwe
    else:
        snwe = list(bbox)
        if len(snwe) != 4:
            raise ValueError('Bounding box should be a list/tuple of length 4')

    #####Geocode one by one
    first = False
    ge = Geocodable()
    for prod in tobeGeocoded:
        objGeo = stdproc.createGeocode('insarapp_geocode_' + os.path.basename(prod).replace('.',''))
        objGeo.configure()

        ####IF statements to check for user configuration
        if objGeo.minimumLatitude is None:
            objGeo.minimumLatitude = snwe[0]

        if objGeo.maximumLatitude is None:
            objGeo.maximumLatitude = snwe[1]

        if objGeo.minimumLongitude is None:
            objGeo.minimumLongitude = snwe[2]

        if objGeo.maximumLongitude is None:
            objGeo.maximumLongitude = snwe[3]

        if objGeo.demCropFilename is None:
            objGeo.demCropFilename = insar.demCropFilename

        objGeo.referenceOrbit = insar.formSLC1.getMocompPosition(1)

        if objGeo.dopplerCentroidConstantTerm is None:
            objGeo.dopplerCentroidConstantTerm = insar.dopplerCentroid.getDopplerCoefficients(inHz=False)[0]

        if objGeo.bodyFixedVelocity is None:
            objGeo.bodyFixedVelocity = v

        if objGeo.spacecraftHeight is None:
            objGeo.spacecraftHeight = h

        if objGeo.numberRangeLooks is None:
            objGeo.numberRangeLooks = insar.numberRangeLooks

        if objGeo.numberAzimuthLooks is None:
            objGeo.numberAzimuthLooks = insar.numberAzimuthLooks

        if objGeo.isMocomp is None:
            objGeo.isMocomp = insar.is_mocomp

        objGeo.stdWriter = stdWriter

        #create the instance of the input image and the appropriate
        #geocode method
        inImage,method = ge.create(prod)
        if objGeo.method is None:
            objGeo.method = method

        if(inImage):
            #demImage = isceobj.createDemImage()
            #IU.copyAttributes(insar.demImage, demImage)
            demImage = insar.demImage.clone()
            objGeo(peg=insar.peg, frame=insar.masterFrame,
                           planet=planet, dem=demImage, tobegeocoded=inImage,
                           geoPosting=None, masterslc=insar.formSLC1)


            recordInputsAndOutputs(self._insar.procDoc, objGeo, "runGeocode",
                                       logger, "runGeocode")

    stdWriter.finalize()

