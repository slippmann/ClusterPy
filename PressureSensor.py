#**********************************************
#
#   Title:  PressureSensor.py
#   Ver:    1.0
#   Autor:  Steven Lippmann
#   Date:   Feb. 11, 2016
#
#-Last Modified-------------------------------
#
#   By:     Steven Lippmann
#   Date:   Feb. 25, 2016
#
#//////////////////////////////////////////////

from ADC import *

"""Constants"""

INT_NumSamples = 50

class MPX2202AP:

    # see datasheet
    PSIPermV = 0.725
    isDifferential = True

    zeroOffset = 0
    newZeroOffset = 0
    zeroCount = 0
    
    def __init__(self, ADC, channel):

        self.Pressure = 0

        self.ADC = ADC
        self.Channel = channel

    def Read(self):

        mV = 0
        count = 0
    
        while (count < INT_NumSamples):
        
            temp = self.ADC.Read(self.Channel, self.isDifferential) 

            if (temp <= 40):
                mV += temp
                count += 1

        mV /= INT_NumSamples
        AbsPressure = mV * self.PSIPermV
        self.AdjustZero(AbsPressure)
        
        self.Pressure = round(AbsPressure - self.zeroOffset, 1)
        
        return self.Pressure

    def AdjustZero(self, newPressure):

        newPressure = round(newPressure, 1)
        
        if(self.newZeroOffset == int(newPressure)):
            self.zeroCount += 1

        else:
            self.newZeroOffset = newPressure
            self.zeroCount = 0
            return
        
        if(self.zeroCount >= 50):
            self.zeroOffset = self.newZeroOffset

        
