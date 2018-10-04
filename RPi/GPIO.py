#########################################################
#
#   Name: GPIO.py
#   Purpose: Testing library for use outside raspberry pi
#
#   Author: Steven Lippmann
#   Date:   June 30, 2016
#
#########################################################

HIGH = "HIGH";
LOW = "LOW";

IN = "INPUT";
OUT = "OUTPUT";

BCM = "BCM";
BOARD = "BOARD";

class Printer:
    isPrint = True;

    def __init__(self):
        return;

def setmode(mode):
    if(printer.isPrint):
        print("GPIO Mode: {}.".format(mode));
    return;

def setup(pin, mode):
    if(printer.isPrint):
        print("Pin {0} set as {1}.".format(pin, mode));
    return;

def setwarnings(isOn):
    printer.isPrint = isOn
    print("Warnings set to {}.".format(isOn));
    return;

def output(pin, status):
    if(printer.isPrint):
        print("Pin {0} is {1}.".format(pin, status));
    return;

def input(pin):
    if(printer.isPrint):
        print("Checking pin {} for input.".format(pin));
    return 0;

def cleanup():
    print("Cleaning up GPIOs");
    return;

printer = Printer()
