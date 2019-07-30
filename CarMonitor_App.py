#**********************************************
#
#   Title:  DigitalCluster
#   Ver:    1.0
#   Autor:  Steven Lippmann
#   Date:   Nov. 23, 2015
#
#-Last Modified-------------------------------
#
#   By:     Steven Lippmann
#   Date:   Feb. 5, 2016
#
#//////////////////////////////////////////////

import time
import os
from CarMonitor_Core import *
from tkinter import *
from VoltGauge import *
from BoostGauge import *
from PyroGauge import *
from PIL import Image, ImageTk
import numpy
from Config import *

#creating the GUI and its components
class GaugeCluster(Frame):
    
    intakePressure = 0
    exhaustTemperature = 0
    voltage = 0

    loopCounter = 0
        
    def __init__(self, master):
        """
        Initialize gauge cluster.
        
        Inputs:
            master - tkinter master

        Returns:
            None
        """

        Frame.__init__(self, master)
        self.master = master

        self.grid()

        if (DEBUG != 1):
        	self.CarManager = Manager()

        self.InitializeImages()

        self.voltGauge = VoltGauge(self.cluster)
        self.boostGauge = BoostGauge(self.cluster)
        self.pyroGauge = PyroGauge(self.cluster)
        
        self.isReady = False

    def InitializeImages(self):
        """
        Loads all of the application images and places them on the tkinter canvas.

        Inputs:
            None

        Returns:
            None
        """

        self.backgroundImage = ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/ClusterBackground.png")
        
        self.boostGaugeImage = ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/BoostGauge.png")
        self.pyroGaugeImage = ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/PyroGauge.png")
        self.voltGaugeImage = ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/VoltGauge.png")

        self.cluster = Canvas(self, width = 800, height = 480)
        self.cluster.create_image(backgroundCentre, image = self.backgroundImage)
        self.cluster.create_image(voltGaugeCentre, image = self.voltGaugeImage)
        self.cluster.create_image(boostGaugeCentre, image = self.boostGaugeImage)
        self.cluster.create_image(pyroGaugeCentre, image = self.pyroGaugeImage)
        
        self.cluster.pack()
        
    def UpdateClusterLoop(self):
        """
        The main loop of the application.
        Reading sensors and updating gauge displays.

        Inputs:
            None

        Returns:
            None
        """

        if self.isReady == False:
            if self.loopCounter == 0:
                self.loopCounter = 1
                self.after(INT_StartUpDelayMilliseconds, self.UpdateClusterLoop)
                return
                
            self.Startup(self.loopCounter)
            
            if self.loopCounter >= INT_StartCycles:
                self.loopCounter = 0
                
                self.boostGauge.UpdateValue(self.intakePressure)
                self.pyroGauge.UpdateValue(self.exhaustTemperature)
                self.voltGauge.UpdateValue(self.voltage)

                self.isReady = True
        
        else:
            self.UpdateBoostGauge()
            self.UpdateVoltGauge()
            self.UpdatePyroGauge()

            if (self.loopCounter >= 10):
                self.loopCounter = 0
        
        self.loopCounter += 1
        
        self.after(INT_RefreshDelayMilliseconds, self.UpdateClusterLoop)

    def UpdateVoltGauge(self):
        """
        Get new value from sensors and update the gauge display.
        Dont update display if the sensor data has not changed.

        Inputs:
            None

        Returns:
            None
        """

        if (DEBUG != 1):
            self.voltage = self.CarManager.UpdateVoltage()

        self.voltGauge.UpdateValue(self.voltage)

    def UpdateBoostGauge(self):
        """
        Get new value from sensors and update the gauge display.
        Dont update display if the sensor data has not changed.

        Inputs:
            None

        Returns:
            None
        """
        
        if (DEBUG != 1):
            self.intakePressure = self.CarManager.UpdatePressure()

        self.boostGauge.UpdateValue(self.intakePressure)
        
    def UpdatePyroGauge(self):
        """
        Get new value from sensors and update the gauge display.
        Dont update display if the sensor data has not changed.

        Inputs:
            None

        Returns:
            None
        """
        
        if (DEBUG != 1):
            self.exhaustTemperature = self.CarManager.UpdateTemperature()
        
        self.pyroGauge.UpdateValue(self.exhaustTemperature)

    def Startup(self, counter):
        """
        Start up sequence for the gauges. 
        
        Inputs:
            None

        Returns:
            None
        """

        half = INT_StartCycles / 2
        stepL = 225 / half
        stepS = 180 / half
        
        if counter <= half:
            angle1 = -45 + stepL * counter
            angle2 = stepS * counter
            self.voltGauge.RotateNeedle(angle2)
            self.boostGauge.RotateNeedle(angle1)
            self.pyroGauge.RotateNeedle(angle1)
        
        else:
            angle1 = -45 + stepL * (half - (counter - half))
            angle2 = stepS * (half - (counter - half))
            self.voltGauge.RotateNeedle(angle2)
            self.boostGauge.RotateNeedle(angle1)
            self.pyroGauge.RotateNeedle(angle1)
        
        if (counter % 8 == 0):
            segmentNumber = (counter / 8)
            self.voltGauge.ShowSegment((segmentNumber + 0) % 6)
            self.boostGauge.ShowSegment((segmentNumber + 2) % 6)
            self.pyroGauge.ShowSegment((segmentNumber + 4) % 6)
            
    def Dispose(self):
        """
        Clean up app and destroy tkinter window

        Inputs:
            None

        Returns:
            None
        """
        self.master.destroy()

    def Demo(self):
        """
        Demo the gauges for debugging purposes

        Inputs:
            None

        Returns:
            None
        """
        if (DEBUG == 1) and (self.isReady):
            self.intakePressure = self.intakePressure + 0.2 if (self.intakePressure + 0.2 <= 25) else 0
            self.exhaustTemperature = self.exhaustTemperature + 2 if (self.exhaustTemperature + 2 <= 1000) else 0
            self.voltage = self.voltage + 0.2 if (self.voltage + 0.2 <= 18) else 0
