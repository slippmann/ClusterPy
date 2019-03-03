from Gauge import *
from Config import *

class PyroGauge(Gauge):

    def __init__(self, canvas):

        self.centre = pyroGaugeCentre
        self.needleDimensions = largeNeedleDimensions
        self.degreesPerUnit = FLOAT_PyroDegreesPerUnit
        self.needleOffset = -45
        self.decimalPrecision = 0

        self.displayOffset = lDisplayOffset
        self.segOffset = lSegOffset

        self.outsideSeg = lSegOutside
        self.middleSeg = lSegMiddle

        super().__init__(canvas)

