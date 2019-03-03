from math import pi
import os
import numpy as np

"""------Coodinates------"""
backgroundCentre = (400, 240)
boostGaugeCentre = (180, 280)
pyroGaugeCentre = (620, 280)
voltGaugeCentre = (400, 150)

#26x48
lDisplayOffset = np.array([[6, 48], [40, 48], [74, 48]])

lSegOffset = np.array([[0,3],[0,25],[3,48],[26,25],[26,3],[3,0],[3,22]])
#lSegOutside = np.array([[2,0],[0,0],[0,20],[2,20],[4,18],[4,2]])
lSegOutside = np.array([[0,0],[0,20],[4,16],[4,4]])
lSegMiddle = np.array([[0,2],[2,0],[18,0],[20,2],[18,4],[2,4]])

#18x32
sDisplayOffset = np.array([[-12, 26], [10, 26], [32, 26]])

sSegOffset = np.array([[0,2],[0,17],[2,32],[18,17],[18,2],[2,0],[2,15]])
sSegOutside = np.array([[0,0],[3,3],[3,11],[0,14]])
sSegMiddle = np.array([[0,1],[1,0],[13,0],[14,1],[13,3],[1,3]])

"""------Dimensions-----"""
largeNeedleDimensions = (152, 8)
smallNeedleDimensions = (102, 6)

"""------Constants------"""
INT_StartUpDelayMilliseconds = 1000
INT_StartCycles = 100
INT_RefreshDelayMilliseconds = 10
STR_WorkingDir = os.getcwd()

FLOAT_BoostDegreesPerUnit = 9.0
FLOAT_PyroDegreesPerUnit = (9.0/40.0)
FLOAT_VoltDegreesPerUnit = 10

FLOAT_Radians2Degrees = pi / 180

INTARR_DigitCode = [\
            (1,1,1,1,1,1,0),\
            (0,0,0,1,1,0,0),\
            (0,1,1,0,1,1,1),\
            (0,0,1,1,1,1,0),\
            (1,0,0,1,1,0,1),\
            (1,0,1,1,0,1,1),\
            (1,1,1,1,0,1,1),\
            (0,0,0,1,1,1,0),\
            (1,1,1,1,1,1,1),\
            (1,0,1,1,1,1,1),\
            (0,0,0,0,0,0,0)] 

"""------Calculations------"""
voltDisplayOffset = []
voltDisplayOffset.append((voltGaugeCentre[0] + sDisplayOffset[0][0], 
                          voltGaugeCentre[1] + sDisplayOffset[0][1]))
voltDisplayOffset.append((voltGaugeCentre[0] + sDisplayOffset[1][0], 
                          voltGaugeCentre[1] + sDisplayOffset[1][1]))
voltDisplayOffset.append((voltGaugeCentre[0] + sDisplayOffset[2][0], 
                          voltGaugeCentre[1] + sDisplayOffset[2][1]))

boostDisplayOffset = []
boostDisplayOffset.append((boostGaugeCentre[0] + lDisplayOffset[0][0], 
                           boostGaugeCentre[1] + lDisplayOffset[0][1]))
boostDisplayOffset.append((boostGaugeCentre[0] + lDisplayOffset[1][0], 
                           boostGaugeCentre[1] + lDisplayOffset[1][1]))
boostDisplayOffset.append((boostGaugeCentre[0] + lDisplayOffset[2][0], 
                           boostGaugeCentre[1] + lDisplayOffset[2][1]))

pyroDisplayOffset = []
pyroDisplayOffset.append((pyroGaugeCentre[0] + lDisplayOffset[0][0], 
                          pyroGaugeCentre[1] + lDisplayOffset[0][1]))
pyroDisplayOffset.append((pyroGaugeCentre[0] + lDisplayOffset[1][0], 
                          pyroGaugeCentre[1] + lDisplayOffset[1][1]))
pyroDisplayOffset.append((pyroGaugeCentre[0] + lDisplayOffset[2][0], 
                          pyroGaugeCentre[1] + lDisplayOffset[2][1]))