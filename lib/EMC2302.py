import time
from machine import I2C
#import math

__version__ = '0.0.1'

class EMC2302:
    """ class for handling the dual fan controller EMC2302
        datasheet available at http://ww1.microchip.com/downloads/en/DeviceDoc/2302.pdf""" 

    EMC2302_I2C_ADDR = const(0x46)

    FAN_1_TACH_LOW = const(0x3F)
    FAN_1_TACH_HI = const(0x3E)
    
    FAN_2_TACH_LOW = const(0x4F)
    FAN_2_TACH_HI = const(0x4E)
    

    def __init__(self, sda = 'P22', scl = 'P21'):
        self.i2c = I2C(0, mode=I2C.MASTER, pins=(sda, scl), baudrate=100000)


    #def Calc_Temp(centicelcius):

