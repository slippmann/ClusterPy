#**********************************************
#
#   Title:  Thermocouple
#   Ver:    1.0
#   Autor:  Steven Lippmann
#   Date:   Feb. 5, 2016
#
#-Last Modified-------------------------------
#
#   By:     Steven Lippmann
#   Date:   Feb. 11, 2016
#
#//////////////////////////////////////////////

import SPI
import RPi.GPIO as GPIO

class MAX31855:

    temperature = 0

    def __init__(self, SPIPort, chipSelect):

        self.CS = chipSelect
        self.SPIPort = SPIPort

        GPIO.setup(self.CS, GPIO.OUT)
        GPIO.output(self.CS, True)

    def Read(self):

        GPIO.output(self.CS, True)
        GPIO.output(self.CS, False)
        
        chipOut = self.SPIPort.Read(14)

        GPIO.output(self.CS, True)

        self.temperature = chipOut >> 3

        return self.temperature

    def Dispose(self):
        """Releases all allocated memory and pin information"""

        self.CS = 0

        self.SPIPort = None
