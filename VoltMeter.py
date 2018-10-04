#**********************************************
#
#   Title:  VoltMeter.py
#   Ver:    1.0
#   Autor:  Steven Lippmann
#   Date:   Jul. 7, 2016
#
#-Last Modified-------------------------------
#
#   By:     Steven Lippmann
#   Date:   Jul. 7, 2016
#
#//////////////////////////////////////////////

from ADC import *

"""Constants"""

INT_NumSamples = 50

class Meter:

    isDifferential = True
    VoltsPermV = 0.0556

    def __init__(self, ADC, channel):

        self.Voltage = 0

        self.ADC = ADC
        self.Channel = channel

    def Read(self):

        mV = 0
        count = 0
    
        while (count < INT_NumSamples):
        
            temp = self.ADC.Read(self.Channel, self.isDifferential) 

            mV += temp
            count += 1

        mV /= INT_NumSamples
        AbsVoltage = mV * self.VoltsPermV
        
        self.Voltage = round(AbsVoltage, 1)
        
        return self.Voltage
    
