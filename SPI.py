#**********************************************
#
#   Title:  SPI.py
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

import os
import RPi.GPIO as GPIO

class Port:

    MOSI = None
    MISO = None
    CLK = None

    def __init__(self, mosi, miso, clk):

        self.MOSI = mosi
        self.MISO = miso
        self.CLK = clk

        GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(self.MOSI, GPIO.OUT)
        GPIO.setup(self.MISO, GPIO.IN)
        GPIO.setup(self.CLK, GPIO.OUT)

    def Send(self, packet):
        
        for i in range(packet.bit_length()):
            if (packet & 0x10):
                GPIO.output(self.MOSI, True)
            else:
                GPIO.output(self.MOSI, False)

            packet <<= 1

            GPIO.output(self.CLK, True)
            GPIO.output(self.CLK, False)
        
    def Read(self, bitsToRead):

        bits = 0

        for i in range(bitsToRead):
            GPIO.output(self.CLK, True)
            GPIO.output(self.CLK, False)

            bits <<= 1

            if (GPIO.input(self.MISO)):
                bits |= 0x1
        
        return bits

    def Dispose(self):

        self.MOSI = 0
        self.MISO = 0
        self.CLK = 0
        
        GPIO.cleanup()
