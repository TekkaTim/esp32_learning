import time
from machine import I2C
#import math

__version__ = '0.0.1'

class EMC2302:
    """ class for handling the dual fan controller EMC2302
        datasheet available at http://ww1.microchip.com/downloads/en/DeviceDoc/2302.pdf""" 

    EMC2302_I2C_ADDR = const(0x46)

    #Configuration and control registers
    FAN_STATUS = const(0x24)
    FAN_STALL_STATUS = const(0x25)
    FAN_SPIN_STATUS = const(0x26)
    DRIVE_FAIL_STATUS = const(0x27)

    #Fan 1 Control registers
    FAN_1_SETTING = const(0x30)
    FAN_1_CONTROL1 = const(0x32)
    FAN_1_CONTROL2 = const(0x33)
    FAN_1_TACH_TARGET_LOW = const(0x3C)
    FAN_1_TACH_TARGET_HI = const(0x3D)
    FAN_1_TACH_READ_LOW = const(0x3F)
    FAN_1_TACH_READ_HI = const(0x3E)
    
    #Fan 2 Control registers
    FAN_2_SETTING = const(0x40)
    FAN_2_CONTROL1 = const(0x42)
    FAN_2_CONTROL2 = const(0x43)
    FAN_2_TACH_TARGET_LOW = const(0x4C)
    FAN_2_TACH_TARGET_HI = const(0x4D)
    FAN_2_TACH_READ_LOW = const(0x4F)
    FAN_2_TACH_READ_HI = const(0x4E)

    #Revision Registers
    EMC2302_PRODUCT_ID = const(0xFD)
    EMC2302_MANUF_ID = const(0xFE)
    EMC2302_REVISION = const(0xFF)


    def __init__(self, sda = 'P22', scl = 'P21'):
        self.i2c = I2C(0, mode=I2C.MASTER, pins=(sda, scl), baudrate=100000)


    #def Calc_Temp(centicelcius):

