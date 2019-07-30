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
from threading import *
from PIL import Image, ImageTk
import numpy as np
import math
from Config import *

class Gauge:
    """
    Base class for all gauges. 
    Handles drawing the needle and populating the digital display.
    """

    centre = None
    needleDimensions = None
    degreesPerUnit = None
    needleOffset = None
    decimalPrecision = None

    displayOffset = None
    segOffset = None

    outsideSeg = None
    middleSeg = None

    # Arrays
    digitPoly = None
    digitNum = None

    def __init__(self, canvas):
        """
        Initialize the gauge.

        Input:
            None

        Returns:
            None
        """

        self.canvas = canvas

        self.value = 0
        self.angle = 0
        self.needle = 0

        self.Configure()

    def Configure(self):
        """
        Configure the gauge.
        This will build the needle and digital display
        then draw them on the tkinter canvas.

        Input:
            None

        Returns:
            None
        """
        try:
            self.BuildNeedle()
            self.BuildDigitalDisplay()

            self.CalculateDigitalDisplay()
            self.CalculateNeedle()

            self.DrawNeedle()
        except:
            raise ValueError("User must set:\n\ncentre, needleDimensions, degreesPerUnit, needleOffset, decimalPrecision, displayOffset, segOffset, outsideSeg, middleSeg\n\nBefore Gauge.__init__()")

    def BuildNeedle(self):
        """
        Build the initial point mapping of the needle.

        Input:
            None

        Returns:
            None
        """

        l1 = self.needleDimensions[0] * 0.8
        l2 = self.needleDimensions[0] * 0.2
        w = self.needleDimensions[1] * 0.5

        self.needleP1 = np.array([-l1   , w     , 1])
        self.needleP2 = np.array([-l1   , -w    , 1])
        self.needleP3 = np.array([l2    , -w    , 1])
        self.needleP4 = np.array([l2    , w     , 1])

        self.needleP1 = self.needleP1.reshape(3,1)
        self.needleP2 = self.needleP2.reshape(3,1)
        self.needleP3 = self.needleP3.reshape(3,1)
        self.needleP4 = self.needleP4.reshape(3,1)

    def BuildDigitalDisplay(self):
        """
        Build the initial segments of the digital display.

        Input:
            None

        Returns:
            None
        """

        digitOffset = self.displayOffset + self.centre

        xflip = np.array([
            [-1, 0],
            [0 , 1]
            ])
        yflip = np.array([
            [1 , 0],
            [0 ,-1]
            ])
        flop = np.array([
            [0 , 1],
            [1 , 0]
            ])

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
        
            for j in range(7):
                self.digitPoly[i][j] = self.canvas.create_polygon(disp[j], fill="#000")

    def CalculateNeedle(self, degrees=None):
        """
        Calculate the point mapping of the needle polygon based on a given rotation

        Input:
            degrees - (Optional) degrees to rotate the needle from 0

        Returns:
            None
        """

        # To rotate the needle without affecting the gauge value
        # Used in start-up sequence
        if (degrees == None):
            self.angle = (self.value * self.degreesPerUnit) + self.needleOffset
        else:
            self.angle = degrees

        s = math.sin(self.angle * FLOAT_Degrees2Radians)
        c = math.cos(self.angle * FLOAT_Degrees2Radians)
        
        rotationMatrix = np.array([
            [c  , -s    , self.centre[0]    ],
            [s  , c     , self.centre[1]    ],
            [0  , 0     , 1                 ]
            ])
    
        self.needleNewP1 = rotationMatrix.dot(self.needleP1).tolist()
        self.needleNewP2 = rotationMatrix.dot(self.needleP2).tolist()
        self.needleNewP3 = rotationMatrix.dot(self.needleP3).tolist()
        self.needleNewP4 = rotationMatrix.dot(self.needleP4).tolist()

    def CalculateDigitalDisplay(self):
        """
        Calculate the 3 digits in the digital display.

        Input:
            None

        Returns:
            None
        """

        value = self.value * (10**self.decimalPrecision)

        self.digitNum[0] = (int(value / 100))
        self.digitNum[1] = (int((value / 10) - (self.digitNum[0] * 10)))
        self.digitNum[2] = (int(value % 10))

        if (self.digitNum[0] <= 0):
            self.digitNum[0] = 10
        elif (self.digitNum[0] > 9):
            self.digitNum[0] = 9
            self.digitNum[1] = 9
            self.digitNum[2] = 9

        if (self.decimalPrecision == 0 and 
			self.digitNum[0] == 10 and self.digitNum[1] == 0):
            self.digitNum[1] = 10             

    def DrawNeedle(self):
        """
        Draws the rotated needle polygon onto the tkinter canvas.

        Input:
            None

        Returns:
            None
        """

        if (self.needle != 0):
            self.canvas.delete(self.needle)

        self.needle = self.canvas.create_polygon(self.needleNewP1[0:2],
                                                 self.needleNewP2[0:2],
                                                 self.needleNewP3[0:2],
                                                 self.needleNewP4[0:2],
                                                 outline="#000",
                                                 fill="#F00",
                                                 width=2)

    def DrawDigitalDisplay(self):
        """
        Draws the digital display polygons onto the tkinter canvas.

        Input:
            None

        Returns:
            None
        """

        for i in range(3):
            for j in range(7):

                if INTARR_DigitCode[self.digitNum[i]][j]:
                    self.canvas.itemconfig(self.digitPoly[i][j], state = "normal")
                else:
                    self.canvas.itemconfig(self.digitPoly[i][j], state = "hidden")

    def ShowSegment(self,segNum):
        """
        Draw a single segment in each of the digital display digits.

        Input:
            segNum - The segment in the display to draw.

        Returns:
            None
        """

        for i in range(3):
            for j in range(7):

                if (j == segNum):
                    self.canvas.itemconfig(self.digitPoly[i][j], state = "normal")
                else:
                    self.canvas.itemconfig(self.digitPoly[i][j], state = "hidden")

    def RotateNeedle(self, degrees):
        """
        Rotates the needle by 'degrees' then draws the needle polygon onto the tkinter canvas.

        Input:
            degrees - degrees to rotate the needle from 0

        Returns:
            None
        """

        self.CalculateNeedle(degrees)
        self.DrawNeedle()

    def UpdateValue(self, value, override=False):
        """
        Update the value of the gauge. 
        This will update the needle and the digital display 
        then draw all of the polygons on the tkinter canvas.

        Input:
            None

        Returns:
            None
        """
       
        if (value == self.value and override == False):
            return
        
        self.value = value

        needleThread = Thread(target=self.CalculateNeedle, args=())
        digitalThread = Thread(target=self.CalculateDigitalDisplay, args=())

        needleThread.start()
        digitalThread.start()

        needleThread.join()
        digitalThread.join()

        self.DrawNeedle()
        self.DrawDigitalDisplay()

