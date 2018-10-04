#**********************************************
#
#   Title:  ADC.py
#   Ver:    1.0
#   Autor:  Steven Lippmann
#   Date:   Nov. 15, 2015
#
#-Last Modified-------------------------------
#
#   By:     Steven Lippmann
#   Date:   Feb. 6, 2016
#
#//////////////////////////////////////////////

import SPI
import RPi.GPIO as GPIO

from Sensor import *

"""Constants"""
Vin = 3.3
R1 = 1.0
R2 = 2.32

Vout = Vin * (R1 / (R1 + R2))

class MCP3008(Sensor):

    Resolution = 1024.0

    def __init__(self, SPIPort, chipSel):    

        Sensor.__init__(self, self.Resolution, chipSel)

        self.mVPerBit = (Vout / self.Resolution) * 1000
        
        self.SPIPort = SPIPort

        self.CS = chipSel
        GPIO.setup(self.CS, GPIO.OUT)

    def Read(self, CH, isDiff):
        """Querys ADC at specified channel(s)"""
    
        if ((CH < 0) or (CH > 7)):
            return -1

        GPIO.output(self.CS, True) # Start high and later bring low to start communication

        GPIO.output(self.CS, False)

        self.StartCommunication(CH, isDiff)
        
        # read one empty bit, one null, 10 data bits
        adcOut = self.SPIPort.Read(12)

        GPIO.output(self.CS, True)

        adcOut >>= 1

        # convert to mV
        mV = adcOut * self.mVPerBit
        
        return mV

    def StartCommunication(self, CH, isDiff):
        """Startup bit sequence
        StartBit | SGL/DIFF | D0 | D1 | D2
        *See Datasheet for details"""

        """differential mode CH is the IN+"""
    
        commandOut = CH

        if isDiff:
            commandOut |= 0x10 # 10000
        else:
            commandOut |= 0x18 # 11000

        self.SPIPort.Send(commandOut)

    def Dispose(self):
        """Releases all allocated memory and pin information"""
        
        self.CS = 0

        self.SPIPort = None
