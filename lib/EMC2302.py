import time
from machine import I2C
#import math

__version__ = '0.0.1'

class EMC2302:
    """ class for handling the dual fan controller EMC2302
        datasheet available at http://ww1.microchip.com/downloads/en/DeviceDoc/2302.pdf""" 

    EMC2302_I2C_ADDR = const(46)
    __EMC2303_READ_WAIT__ = 0.1

    #Configuration and control registers
    CONFIG_REGISTER = const(0x20)
    FAN_STATUS = const(0x24)
    FAN_STALL_STATUS = const(0x25)
    FAN_SPIN_STATUS = const(0x26)
    DRIVE_FAIL_STATUS = const(0x27)

    #Fan 1 Control registers
    FAN_1_SETTING = const(0x30)
    FAN_1_CONTROL1 = const(0x32)
    FAN_1_CONTROL2 = const(0x33)
    FAN_1_TACH_TARGET_LOW = const(0x3C)
    FAN_1_TACH_TARGET_HIGH = const(0x3D)
    FAN_1_TACH_READ_LOW = const(0x3F)
    FAN_1_TACH_READ_HIGH = const(0x3E)
    
    #Fan 2 Control registers
    FAN_2_SETTING = const(0x40)
    FAN_2_CONTROL1 = const(0x42)
    FAN_2_CONTROL2 = const(0x43)
    FAN_2_TACH_TARGET_LOW = const(0x4C)
    FAN_2_TACH_TARGET_HIGH = const(0x4D)
    FAN_2_TACH_READ_LOW = const(0x4F)
    FAN_2_TACH_READ_HIGH = const(0x4E)

    #Revision Registers
    EMC2302_PRODUCT_ID = const(0xFD)
    EMC2302_MANUF_ID = const(0xFE)
    EMC2302_REVISION = const(0xFF)


    def __init__(self, sda = 'P22', scl = 'P21'):
        self.i2ctim = I2C(0, mode=I2C.MASTER, pins=(sda, scl), baudrate=100000)
        print("Scanning I2C Bus...")
        bob=self.i2ctim.scan()
        print("Found - ",bob)



    #def Calc_Temp(centicelcius):



    def product_id(self):
        """ Gets the Product ID from the Fan Controller Chip (should be 0x36) """
        self.i2ctim.writeto(EMC2302_I2C_ADDR, EMC2302_PRODUCT_ID)
        time.sleep(0.1)
        data = self.i2ctim.readfrom(EMC2302_I2C_ADDR, 1)
        return data

    def manufacturer_id(self):
        """ Gets the Manufacturer ID from the Fan Controller Chip (should be 0x5D) """
        self.i2ctim.writeto(EMC2302_I2C_ADDR, EMC2302_MANUF_ID)
        time.sleep(0.1)
        manu_id = self.i2ctim.readfrom(EMC2302_I2C_ADDR, 1)
        return manu_id

    def revision(self):
        """ Gets the Revision from the Fan Controller Chip (should be 0x80) """
        self.i2ctim.writeto(EMC2302_I2C_ADDR, EMC2302_REVISION)
        time.sleep(0.1)
        rev = self.i2ctim.readfrom(EMC2302_I2C_ADDR, 1)
        return rev

    def fan_status(self):
        """ Get the Fan Status
             The Fan Status register (0x24) indicates that one or both of the fan
             drivers has stalled or failed or that the Watchdog Timer has expired.
             Bits of interest are 7 (Watchdog), 2 (Drive), 1 (Spin) and 0 (Stall) """
        self.i2ctim.writeto(EMC2302_I2C_ADDR, FAN_STATUS)
        time.sleep(0.1)
        data = self.i2ctim.readfrom(EMC2302_I2C_ADDR, 1)
        fanstatus = [0,0,0,0]
        fanstatus[0] = data[0] & 1
        fanstatus[1] = data[0] >> 1 & 1
        fanstatus[2] = data[0] >> 2 & 1
        fanstatus[3] = data[0] >> 7 & 1
        return fanstatus

    def fan_stall_status(self):
        """ Get the Fan Stall Status
             The Fan Stall Status register indicates which fan driver has detected
             a stalled condition. "1" = fault
             All bits are cleared upon a read if the error condition has been removed.
             Bits of interest are 1 (Fan 2) and 0 (Fan 1) """
        self.i2ctim.writeto(EMC2302_I2C_ADDR, FAN_STALL_STATUS)
        time.sleep(0.1)
        data = self.i2ctim.readfrom(EMC2302_I2C_ADDR, 1)
        fanstallstatus = [0,0]
        fanstallstatus[0] = data[0] & 1
        fanstallstatus[1] = data[0] >> 1 & 1
        return fanstallstatus

    def fan_spin_status(self):
        """ Get the Fan Spin Status
             The Fan Stall Status register indicates which fan driver has failed
             to spin-up. "1" = fault
             All bits are cleared upon a read if the error condition has been removed.
             Bits of interest are 1 (Fan 2) and 0 (Fan 1) """
        self.i2ctim.writeto(EMC2302_I2C_ADDR, FAN_SPIN_STATUS)
        time.sleep(0.1)
        data = self.i2ctim.readfrom(EMC2302_I2C_ADDR, 1)
        fanspinstatus = [0,0]
        fanspinstatus[0] = data[0] & 1
        fanspinstatus[1] = data[0] >> 2 & 1
        return fanspinstatus

    def fan_drive_fail_status(self):
        """ Get the Fan Drive Fail Status
             The Fan Stall Status register indicates which fan driver has detected
             a stalled condition. "1" = fault
             All bits are cleared upon a read if the error condition has been removed.
             Bits of interest are 1 (Fan 2) and 0 (Fan 1) """
        self.i2ctim.writeto(EMC2302_I2C_ADDR, DRIVE_FAIL_STATUS)
        time.sleep(0.1)
        data = self.i2ctim.readfrom(EMC2302_I2C_ADDR, 1)
        fandrivestatus = [0,0]
        fandrivestatus[0] = data[0] & 1
        fandrivestatus[1] = data[0] >> 2 & 1
        return fandrivestatus

    def fan_rpm(self):
        """ Get the RPM of Fan
             The The TACH Reading Registers’ contents describe the current tachometer
             reading for each of the fans. By default, the data represents the fan
             speed as the number of 32kHz clock periods that occur for a single
             revolution of the fan.
             There are 2 Bytes in this measurement, with the lowest byte being bit
             shifted 3 times to the left (?) """
        fanrpm=[0,0,0,0]
        self.i2ctim.writeto(EMC2302_I2C_ADDR, FAN_1_TACH_TARGET_LOW)
        time.sleep(0.1)
        data = self.i2ctim.readfrom(EMC2302_I2C_ADDR, 1)
        fanrpm[0] = data[0]
        self.i2ctim.writeto(EMC2302_I2C_ADDR, FAN_1_TACH_TARGET_HIGH)
        time.sleep(0.1)
        data= self.i2ctim.readfrom(EMC2302_I2C_ADDR, 1)
        fanrpm[1] = data[0]

        self.i2ctim.writeto(EMC2302_I2C_ADDR, FAN_2_TACH_TARGET_LOW)
        time.sleep(0.1)
        data = self.i2ctim.readfrom(EMC2302_I2C_ADDR, 1)
        fanrpm[2] = data[0]
        self.i2ctim.writeto(EMC2302_I2C_ADDR, FAN_2_TACH_TARGET_HIGH)
        time.sleep(0.1)
        data= self.i2ctim.readfrom(EMC2302_I2C_ADDR, 1)
        fanrpm[3] = data[0]
        return fanrpm

    def get_config_register(self):
        """ Get setting from the Configuration Register (0x20).
             The Configuration Register controls the basic functionality of the
             EMC2302 fan controller.
             Bits of interest are;
               * 7 - Alert Pin masked. 0 (def): pin enabled, 1: pin disabled
               * 6 - Disable SMB timout - for I2C compatibility
               * 5 - Watchdog - 0 (def): single shot, 1: continuous
               * 1 - CLK output - 0 (def): input, 1: output
               * 0 - CLK Source - 0 (def): internal, 1: external
        """
        self.i2ctim.writeto(EMC2302_I2C_ADDR, CONFIG_REGISTER)
        time.sleep(0.1)
        data = self.i2ctim.readfrom(EMC2302_I2C_ADDR, 1)
        configregister = data[0]
        return configregister


