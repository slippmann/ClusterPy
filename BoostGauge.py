from Gauge import *
from Config import *

class BoostGauge(Gauge):

    def __init__(self, canvas):

        self.centre = boostGaugeCentre
        self.needleDimensions = largeNeedleDimensions
        self.degreesPerUnit = FLOAT_BoostDegreesPerUnit
        self.needleOffset = -45
        self.decimalPrecision = 1

        self.displayOffset = lDisplayOffset
        self.segOffset = lSegOffset

        self.outsideSeg = lSegOutside
        self.middleSeg = lSegMiddle

        # Arrays
        self.digitPoly = [ [ None for j in range(7) ] for i in range(3) ]
        self.digitNum =  [ None for i in range(3) ]

        super().__init__(canvas)
