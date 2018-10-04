#**********************************************
#
#   Title:  Sensor.py
#   Ver:    1.0
#   Autor:  Steven Lippmann
#   Date:   Feb. 6, 2016
#
#-Last Modified-------------------------------
#
#   By:     Steven Lippmann
#   Date:   Feb. 6, 2016
#
#//////////////////////////////////////////////

import RPi.GPIO as GPIO

class Sensor:
    
    def __init__(self, resolutionBits, chipSelect):
        
        self.Resolution = resolutionBits
        self.CS = chipSelect

        GPIO.setup(self.CS, GPIO.OUT)
        GPIO.output(self.CS, True)
        
