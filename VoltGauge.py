from Gauge import *
from Config import *

class VoltGauge(Gauge):

    def __init__(self, canvas):

        self.centre = voltGaugeCentre
        self.needleDimensions = smallNeedleDimensions
        self.degreesPerUnit = FLOAT_VoltDegreesPerUnit
        self.needleOffset = 0
        self.decimalPrecision = 1

        self.displayOffset = sDisplayOffset
        self.segOffset = sSegOffset

        self.outsideSeg = sSegOutside
        self.middleSeg = sSegMiddle

        # Arrays
        self.digitPoly = [ [ None for j in range(7) ] for i in range(3) ]
        self.digitNum =  [ None for i in range(3) ]

        super().__init__(canvas)
