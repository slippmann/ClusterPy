#**********************************************
#
#   Title:  Gauge
#   Ver:    2.0
#   Autor:  Steven Lippmann
#   Date:   Nov. 23, 2015
#
#-Last Modified-------------------------------
#
#   By:     Steven Lippmann
#   Date:   Jan. 2, 2016
#
#//////////////////////////////////////////////

import os
from PIL import Image, ImageTk
import numpy as np
import math
from Config import *

class Gauge:

    centre = None
    needleDimensions = None
    degreesPerUnit = None
    needleOffset = None
    decimalPrecision = None

    displayOffset = None
    segOffset = None

    outsideSeg = None
    middleSeg = None

    def __init__(self, canvas):
        
        self.canvas = canvas

        self.value = 0
        self.angle = 0
        self.needle = 0

        self.Configure()

    def Configure(self):

        try:
            self.DrawNeedle()
            self.DrawDigitalDisplay()
            self.RotateNeedle(self.needleOffset)
        except:
            raise ValueError("User must set:\n\ncentre, needleDimensions, degreesPerUnit, needleOffset, decimalPrecision, displayOffset, segOffset, outsideSeg, middleSeg\n\nBefore Gauge.__init__()")

    def DrawNeedle(self):

        l1 = self.needleDimensions[0] * 0.8
        l2 = self.needleDimensions[0] * 0.2
        w = self.needleDimensions[1] * 0.5

        self.p1 = np.array([-l1, w, 1])
        self.p2 = np.array([-l1, -w, 1])
        self.p3 = np.array([l2, -w, 1])
        self.p4 = np.array([l2, w, 1])

        self.p1 = self.p1.reshape(3,1)
        self.p2 = self.p2.reshape(3,1)
        self.p3 = self.p3.reshape(3,1)
        self.p4 = self.p4.reshape(3,1)

    def DrawDigitalDisplay(self):
        
        digitOffset = self.displayOffset + self.centre

        xflip = np.array([[-1,0],[0,1]])
        yflip = np.array([[1,0],[0,-1]])
        flop = np.array([[0,1],[1,0]])

        self.digit = []
        for i in range(3):
            offset = self.segOffset + digitOffset[i]
            disp = []
            disp.append((self.outsideSeg + offset[0]).tolist())
            disp.append((self.outsideSeg + offset[1]).tolist())
            disp.append((self.outsideSeg.dot(flop).dot(yflip) + offset[2]).tolist())
            disp.append((self.outsideSeg.dot(xflip) + offset[3]).tolist())
            disp.append((self.outsideSeg.dot(xflip) + offset[4]).tolist())
            disp.append((self.outsideSeg.dot(flop) + offset[5]).tolist())
            disp.append((self.middleSeg + offset[6]).tolist())
        
            self.digit.append([])
            for j in range(7):
                self.digit[i].append(self.canvas.create_polygon(disp[j], fill="#000"))

    def UpdateValue(self, value):

        self.value = value

        self.UpdateNeedle()
        self.UpdateDigitalDisplay()

    def UpdateDigitalDisplay(self):

        value = self.value * (10**self.decimalPrecision)

        number = []
        number.append(int(value / 100))
        number.append(int((value / 10) - (number[0] * 10)))
        number.append(int(value % 10))

        if (number[0] <= 0):
            number[0] = 10
        elif (number[0] > 9):
            number[0] = 9
            number[1] = 9
            number[2] = 9

        if (self.decimalPrecision == 0 and number[1] == 0):
            number[1] = 10

        for i in range(3):
            for j in range(7):
                if INTARR_DigitCode[number[i]][j]:
                    self.canvas.itemconfig(self.digit[i][j], state = "normal")
                else:
                    self.canvas.itemconfig(self.digit[i][j], state = "hidden")
        

    def UpdateNeedle(self):

        self.angle = (self.value * self.degreesPerUnit) + self.needleOffset

        self.RotateNeedle(self.angle)

    def RotateNeedle(self, degrees):

        self.angle = degrees

        if (self.needle != 0):
            self.canvas.delete(self.needle)

        s = math.sin(degrees * FLOAT_Radians2Degrees)
        c = math.cos(degrees * FLOAT_Radians2Degrees)
        
        rotationMatrix = np.array([[c, -s, self.centre[0]], [s, c, self.centre[1]], [0, 0, 1]])
    
        newP1 = rotationMatrix.dot(self.p1).tolist()
        newP2 = rotationMatrix.dot(self.p2).tolist()
        newP3 = rotationMatrix.dot(self.p3).tolist()
        newP4 = rotationMatrix.dot(self.p4).tolist()

        self.needle = self.canvas.create_polygon(newP1[0:2], newP2[0:2], newP3[0:2], newP4[0:2], outline="#000", fill="#F00", width=2)

