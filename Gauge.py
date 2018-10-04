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

"""------Constants------"""
STR_WorkingDir = os.getcwd()

degreesPerUnitIMP = -9.0
degreesPerUnitEGT = -(9.0/40.0)
degreesPerUnitVolt = -10

class GaugeType:
    Boost = 1
    Pyro = 2
    Volt = 3

class Gauge:
    
    def __init__(self, background, gaugeType):
        
        self.value = 0
        self.angle = 45

        self.gaugeType = gaugeType

        if (self.gaugeType == GaugeType.Boost):
            self.degreesPerUnit = degreesPerUnitIMP
            
        elif (self.gaugeType == GaugeType.Pyro):
            self.degreesPerUnit = degreesPerUnitEGT
            
        elif (self.gaugeType == GaugeType.Volt):
            self.degreesPerUnit = degreesPerUnitVolt

        else:
            raise TypeError("Unknown Gauge type: {}".format(self.gaugeType));

        self.Background = background

        self.InitializeImages()

        self.Needle = ImageTk.PhotoImage(self.needlePNG)
        self.Digital = [self.digitalImages[10], self.digitalImages[10], self.digitalImages[10]]

    def InitializeImages(self):
        
        if (self.gaugeType == GaugeType.Boost or self.gaugeType == GaugeType.Pyro):
            self.needlePNG = Image.open(STR_WorkingDir + "/Images/GaugeNeedle.png")
            
            self.digitalImages = [\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Zero.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/One.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Two.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Three.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Four.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Five.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Six.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Seven.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Eight.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Nine.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Empty.png")]
        else:
            self.needlePNG = Image.open(STR_WorkingDir + "/Images/VoltNeedle.png")
            
            self.digitalImages = [\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Zero-Small.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/One-Small.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Two-Small.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Three-Small.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Four-Small.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Five-Small.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Six-Small.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Seven-Small.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Eight-Small.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Nine-Small.png"),\
            ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/Empty-Small.png")]

    def UpdateValue(self, value):

        self.value = value

        self.UpdateNeedle()
        self.UpdateDigitalDisplay()

    def UpdateDigitalDisplay(self):

        value = self.value

        if (self.gaugeType == GaugeType.Boost or self.gaugeType == GaugeType.Volt):
            value *= 10

        first = int(value / 100)
        second = int((value / 10) - (first * 10))
        third = int(value % 10)

        if (first <= 0):
            first = 10
        elif (first > 9):
            first = 9

        if (self.gaugeType == GaugeType.Pyro and second == 0):
            second = 10

        self.Digital[0] = self.digitalImages[first]
        self.Digital[1] = self.digitalImages[second]
        self.Digital[2] = self.digitalImages[third]
        

    def UpdateNeedle(self):

        self.angle = (self.value * self.degreesPerUnit)

        if (self.gaugeType != GaugeType.Volt):
            self.angle += 45
        
        self.Needle = ImageTk.PhotoImage(self.needlePNG.rotate(self.angle))
