from math import pi
import os
import numpy as np

DEBUG = 0

"""------Functions-------"""
def CreateSegment(size, dims):
    length = dims[0]
    width = dims[1]

    segOutside = np.array([                         # Layout for segments around the outside of the display (0,0 is top left. positive y is downward) 
        [0      ,   0               ],              #                          
        [0      ,   length          ],              #  0                   
        [width  ,   length-width    ],              #  |\       
        [width  ,   width           ]               #  | 3               
        ])                                          #  | | 
                                                    #  | 2 
                                                    #  |/ 
                                                    #  1 

    segMiddle = np.array([                         # Layout for the segment in the middle of the display (0,0 is top left. positive y is downward)
        [0              ,  width/2  ],              #
        [width/2        ,  0        ],              #  
        [length-width/2 ,  0        ],              #     1________2
        [length         ,  width/2  ],              #  0 < ________ > 3
        [length-width/2 ,  width    ],              #     5        4
        [width/2        ,  width    ]               #
        ])                                          #

    padding = (                                     # Space from edge of display area to start of a segment
        (size[0] - segOutside[1][1]) / 2,           # x padding
        ((size[1] / 2) - segOutside[1][1]) / 2      # y padding
        )

    segOffset = np.array([                                         
        [0          ,   padding[1]                  ],      # Offsets for each segment (0,0 is top left. positive y is downward)                          
        [0          ,   ((size[1]+padding[1])/2)    ],      #    _______        
        [padding[0] ,   size[1]                     ],      #   \___5___/                         
        [size[0]    ,   ((size[1]+padding[1])/2)    ],      # |\         /|        
        [size[0]    ,   padding[1]                  ],      # |0|       |4|                          
        [padding[0] ,   0                           ],      # |/  _____  \|                                   
        [padding[0] ,   ((size[1]/2)-width/2)       ]       #    <__6__>          
        ])                                                  # |\         /|
                                                            # |1|       |3|
                                                            # |/  _____  \|
                                                            #    /__2__\

    return [segOutside, segMiddle, segOffset]

"""------Coodinates------"""
backgroundCentre = (400, 240)
boostGaugeCentre = (180, 280)
pyroGaugeCentre = (620, 280)
voltGaugeCentre = (400, 150)

# 7-Segment size 26x48px
dispArea = (26,48)
segDims = (22,4)
[lSegOutside, lSegMiddle, lSegOffset] = CreateSegment(dispArea,segDims)

lDisplayOffset = np.array([     # Offset from gauge center
    [6, 48],                    # First digit
    [40, 48],                   # Second digit
    [74, 48]                    # Third digit
    ])


# 7-Segment size 18x32px
dispArea = (18,32)
segDims = (14,3)
[sSegOutside, sSegMiddle, sSegOffset] = CreateSegment(dispArea,segDims)

sDisplayOffset = np.array([     # See above for description
    [-12, 26],
    [10, 26],
    [32, 26]
    ])

"""------Dimensions-----"""
largeNeedleDimensions = (152, 8)
smallNeedleDimensions = (102, 6)

"""------Constants------"""
INT_StartUpDelayMilliseconds = 1000
INT_StartCycles = 100
INT_RefreshDelayMilliseconds = 10
STR_WorkingDir = os.path.dirname(os.path.realpath(__file__))

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