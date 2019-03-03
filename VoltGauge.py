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

        super().__init__(canvas)
