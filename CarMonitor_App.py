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
    
    intakePressure = 25
    exhaustTemperature = 1000
    voltage = 18

    loopCounter = 0
        
    def __init__(self, master):
        
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

        if self.isReady == False:
            if self.loopCounter == 0:
                self.loopCounter = 1
                self.after(INT_StartUpDelayMilliseconds, self.UpdateClusterLoop)
                return
                
            self.Startup(self.loopCounter)
            
            if self.loopCounter >= INT_StartCycles:
                self.loopCounter = 0;
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

        temp = self.voltage

        if (DEBUG != 1):
        	self.voltage = self.CarManager.UpdateVoltage()

        	if (temp == self.voltage):
            		return

        self.voltGauge.UpdateValue(self.voltage)

    def UpdateBoostGauge(self):

        temp = self.intakePressure
	
	if (DEBUG != 1):
        	self.intakePressure = self.CarManager.UpdatePressure()

        	if (temp == self.intakePressure):
            		return

        self.boostGauge.UpdateValue(self.intakePressure)
        
    def UpdatePyroGauge(self):

        temp = self.exhaustTemperature
        
        if (DEBUG != 1):
        	self.exhaustTemperature = self.CarManager.UpdateTemperature()

        	if (temp == self.exhaustTemperature):
            		return
        
        self.pyroGauge.UpdateValue(self.exhaustTemperature)

    def Startup(self, counter):
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
            
    def Dispose(self):
        self.master.destroy()
