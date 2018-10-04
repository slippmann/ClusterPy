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
from Gauge import *
from PIL import Image, ImageTk

"""------Coodinates------"""
backgroundCenter = (400, 240)
boostGaugeCenter = (200, 280)
pyroGaugeCenter = (600, 280)
voltGaugeCenter = (400, 150)

voltDisplayZeroOffset = (-3, 42)
voltDisplayOneOffset = (19, 42)
voltDisplayTwoOffset = (41, 42)

displayZeroOffset = (18, 72)
displayOneOffset = (52, 72)
displayTwoOffset = (87, 72)

voltDisplayZero = (voltGaugeCenter[0] + voltDisplayZeroOffset[0], voltGaugeCenter[1] + voltDisplayZeroOffset[1])
voltDisplayOne = (voltGaugeCenter[0] + voltDisplayOneOffset[0], voltGaugeCenter[1] + voltDisplayOneOffset[1])
voltDisplayTwo =(voltGaugeCenter[0] + voltDisplayTwoOffset[0], voltGaugeCenter[1] + voltDisplayTwoOffset[1])

boostDisplayZero = (boostGaugeCenter[0] + displayZeroOffset[0], boostGaugeCenter[1] + displayZeroOffset[1])
boostDisplayOne = (boostGaugeCenter[0] + displayOneOffset[0], boostGaugeCenter[1] + displayOneOffset[1])
boostDisplayTwo =(boostGaugeCenter[0] + displayTwoOffset[0], boostGaugeCenter[1] + displayTwoOffset[1])

pyroDisplayZero = (pyroGaugeCenter[0] + displayZeroOffset[0], pyroGaugeCenter[1] + displayZeroOffset[1])
pyroDisplayOne = (pyroGaugeCenter[0] + displayOneOffset[0], pyroGaugeCenter[1] + displayOneOffset[1])
pyroDisplayTwo = (pyroGaugeCenter[0] + displayTwoOffset[0], pyroGaugeCenter[1] + displayTwoOffset[1])

"""------Constants------"""
INT_RefreshDelayMilliseconds = 20
STR_WorkingDir = os.getcwd()

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

        self.CarManager = Manager()

        self.InitializeImages()

        self.voltGauge = Gauge(self.voltGaugeImage, GaugeType.Volt)
        self.boostGauge = Gauge(self.boostGaugeImage, GaugeType.Boost)
        self.pyroGauge = Gauge(self.pyroGaugeImage, GaugeType.Pyro)

        self.isSimulation = False
        self.isBoost = True

        self.CreateImages()

    def InitializeImages(self):

        self.backgroundImage = ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/ClusterBackground.png")
        
        self.boostGaugeImage = ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/BoostGauge.png")
        self.pyroGaugeImage = ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/PyroGauge.png")
        self.voltGaugeImage = ImageTk.PhotoImage(file = STR_WorkingDir + "/Images/VoltGauge.png")
    
    def CreateImages(self):
        
        self.cluster = Canvas(self, width = 800, height = 480)
        self.cluster.create_image(backgroundCenter, image = self.backgroundImage)
        self.cluster.create_image(voltGaugeCenter, image = self.voltGauge.Background)
        self.cluster.create_image(boostGaugeCenter, image = self.boostGauge.Background)
        self.cluster.create_image(pyroGaugeCenter, image = self.pyroGauge.Background)

        self.voltNeedle = self.cluster.create_image(voltGaugeCenter, image = self.voltGauge.Needle)
        self.voltDisplayZero = self.cluster.create_image(voltDisplayZero, image = self.boostGauge.Digital[0])
        self.voltDisplayOne = self.cluster.create_image(voltDisplayOne, image = self.boostGauge.Digital[1])
        self.voltDisplayTwo = self.cluster.create_image(voltDisplayTwo, image = self.boostGauge.Digital[2])
        
        self.boostNeedle = self.cluster.create_image(boostGaugeCenter, image = self.boostGauge.Needle)
        self.boostDisplayZero = self.cluster.create_image(boostDisplayZero, image = self.boostGauge.Digital[0])
        self.boostDisplayOne = self.cluster.create_image(boostDisplayOne, image = self.boostGauge.Digital[1])
        self.boostDisplayTwo = self.cluster.create_image(boostDisplayTwo, image = self.boostGauge.Digital[2])
        
        self.pyroNeedle = self.cluster.create_image(pyroGaugeCenter, image = self.pyroGauge.Needle)
        self.pyroDisplayZero = self.cluster.create_image(pyroDisplayZero, image = self.pyroGauge.Digital[0])
        self.pyroDisplayOne = self.cluster.create_image(pyroDisplayOne, image = self.pyroGauge.Digital[1])
        self.pyroDisplayTwo = self.cluster.create_image(pyroDisplayTwo, image = self.pyroGauge.Digital[2])
        
        self.cluster.pack()

    def UpdateClusterLoop(self):

        self.UpdateBoostGauge()

        if (self.loopCounter >= 10):
            time.sleep(0.1)
            self.UpdateVoltGauge()
            
            time.sleep(0.1)
            self.UpdatePyroGauge()
            
            self.loopCounter = 0

        self.loopCounter += 1
        
        self.after(INT_RefreshDelayMilliseconds, self.UpdateClusterLoop)

    def UpdateVoltGauge(self):

        temp = self.voltage

        self.voltage = self.CarManager.UpdateVoltage()

        if (temp == self.voltage and self.voltage > 0):
            return

        self.voltGauge.UpdateValue(self.voltage)
        
        self.cluster.itemconfig(self.voltNeedle, image = self.voltGauge.Needle)
        self.cluster.itemconfig(self.voltDisplayZero, image = self.voltGauge.Digital[0])
        self.cluster.itemconfig(self.voltDisplayOne, image = self.voltGauge.Digital[1])
        self.cluster.itemconfig(self.voltDisplayTwo, image = self.voltGauge.Digital[2])

    def UpdateBoostGauge(self):

        temp = self.intakePressure

        self.intakePressure = self.CarManager.UpdatePressure()

        if (temp == self.intakePressure and self.intakePressure > 0):
            return

        self.boostGauge.UpdateValue(self.intakePressure)
        
        self.cluster.itemconfig(self.boostNeedle, image = self.boostGauge.Needle)
        self.cluster.itemconfig(self.boostDisplayZero, image = self.boostGauge.Digital[0])
        self.cluster.itemconfig(self.boostDisplayOne, image = self.boostGauge.Digital[1])
        self.cluster.itemconfig(self.boostDisplayTwo, image = self.boostGauge.Digital[2])
        
    def UpdatePyroGauge(self):

        temp = self.exhaustTemperature
        
        self.exhaustTemperature = self.CarManager.UpdateTemperature()

        if (temp == self.exhaustTemperature and self.exhaustTemperature > 0):
            return
        
        self.pyroGauge.UpdateValue(self.exhaustTemperature)
        
        self.cluster.itemconfig(self.pyroNeedle, image = self.pyroGauge.Needle)
        self.cluster.itemconfig(self.pyroDisplayZero, image = self.pyroGauge.Digital[0])
        self.cluster.itemconfig(self.pyroDisplayOne, image = self.pyroGauge.Digital[1])
        self.cluster.itemconfig(self.pyroDisplayTwo, image = self.pyroGauge.Digital[2])

    def BoostSimulation(self):
        
        if (self.intakePressure >= 17):
            self.isBoost = False
        elif (self.intakePressure <= 0):
            self.isBoost = True
        
        if (self.isBoost):
            self.intakePressure += 0.5
        else:
            self.intakePressure -= 1

        self.boostGauge.UpdateValue(self.intakePressure)
        
    def PyroSimulation(self):
        
        if (self.isBoost):
            self.exhaustTemperature += 8
        else:
            self.exhaustTemperature -= 16

        self.pyroGauge.UpdateValue(self.exhaustTemperature)

    def Startup(self):

        INT_StartupDelayMilliseconds = 2
        
        if (self.intakePressure == 0):
            self.isBoost = True
        elif (self.intakePressure >= 25):
            self.isBoost = False
        
        if (self.isBoost):
            self.intakePressure += 1
            self.exhaustTemperature += 40
        else:
            self.intakePressure -= 1
            self.exhaustTemperature -= 40

        self.boostGauge.UpdateValue(self.intakePressure)
        self.pyroGauge.UpdateValue(self.exhaustTemperature)

        self.UpdateBoostGauge()
        self.UpdatePyroGauge()

        if (self.intakePressure > 0):
            self.after(INT_StartupDelayMilliseconds, self.Startup)
        else:   
            self.UpdateClusterLoop()

    def Dispose(self):

        self.master.destroy()
