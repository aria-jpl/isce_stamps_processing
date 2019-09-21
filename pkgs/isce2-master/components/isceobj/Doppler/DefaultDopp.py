#!usr/bin/env python

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright 2013 California Institute of Technology. ALL RIGHTS RESERVED.
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
# Author: Piyush Agram
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



from __future__ import print_function
import sys
import numpy as np
from iscesys.Component.Component import Component, Port

class DefaultDopp(Component):
   
    def calculateDoppler(self):
        print('Using default doppler values for sensor: %s'%(self._sensor.__class__.__name__))
        self.activateInputPorts()
        pass

    def fitDoppler(self):
        pass

    def addSensor(self):
        sensor = self._inputPorts.getPort('sensor').getObject()
        self._sensor =  sensor
        if (sensor):
            self.quadratic = sensor.extractDoppler()  #insarapp
            self.coeff_list = sensor.frame._dopplerVsPixel #roiApp
            self.prf = sensor.frame.getInstrument().getPulseRepetitionFrequency()

    logging_name = 'DefaultDopp'

    def __init__(self):
        super(DefaultDopp, self).__init__()
        self._sensor = None
        self.quadratic = {}
        self.coeff_list = None
        self.prf = None
        return None

    def createPorts(self):
        sensorPort = Port(name='sensor',method=self.addSensor)
        self._inputPorts.add(sensorPort)
        return None


if __name__ == '__main__':
    pass
