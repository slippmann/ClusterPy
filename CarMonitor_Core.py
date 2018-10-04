#CarMonitor Core file

import SPI
import ADC
import VoltMeter
import Thermocouple
import PressureSensor

"""Pins"""
Vin = 17
GND = 9

ThermocoupleCS = 13
ADConverterCS = 15

mosi = 19
miso = 21
clock = 23

"""Constants"""

PressureSensorCH = 0
VoltMeterCH = 2

class Manager:
        
        def __init__(self):

                self.SPIPort = SPI.Port(mosi, miso, clock)
                self.ADConverter = ADC.MCP3008(self.SPIPort, ADConverterCS)
                self.VoltMeter = VoltMeter.Meter(self.ADConverter, VoltMeterCH)
                self.BoostSensor = PressureSensor.MPX2202AP(self.ADConverter, PressureSensorCH)
                self.EGTSensor = Thermocouple.MAX31855(self.SPIPort, ThermocoupleCS)

        def UpdatePressure(self):

                return self.BoostSensor.Read()

        def UpdateTemperature(self):

                return self.EGTSensor.Read()

        def UpdateVoltage(self):

                return self.VoltMeter.Read()
