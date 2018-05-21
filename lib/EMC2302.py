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
    FAN_1_CONFIG1 = const(0x32)
    FAN_1_CONFIG2 = const(0x33)
    FAN_1_TACH_TARGET_LOW = const(0x3C)
    FAN_1_TACH_TARGET_HIGH = const(0x3D)
    FAN_1_TACH_READ_LOW = const(0x3F)
    FAN_1_TACH_READ_HIGH = const(0x3E)
    
    #Fan 2 Control registers
    FAN_2_SETTING = const(0x40)
    FAN_2_CONFIG1 = const(0x42)
    FAN_2_CONFIG2 = const(0x43)
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

    def read_EMC2302(self, REGISTER, BYTES=1):
        """ Reads a register from the EMC2302 Fan Controller Chip """
        self.i2ctim.writeto(EMC2302_I2C_ADDR, REGISTER)
        time.sleep(0.1)
        data = self.i2ctim.readfrom(EMC2302_I2C_ADDR, BYTES)
        return data

    def write_EMC2302(self, REGISTER, VALUE):
        """ Writes a value to a register in the EMC2302 Fan Controller Chip """
        self.i2ctim.writeto(EMC2302_I2C_ADDR, bytearray([REGISTER])+bytearray([VALUE]))
        time.sleep(0.1)


    def product_id(self):
        """ Gets the Product ID from the Fan Controller Chip (should be 0x36) """
        prod_id = self.read_EMC2302(EMC2302_PRODUCT_ID)
        return prod_id[0]

    def manufacturer_id(self):
        """ Gets the Manufacturer ID from the Fan Controller Chip (should be 0x5D) """
        manu_id = self.read_EMC2302(EMC2302_MANUF_ID)
        return manu_id[0]

    def revision(self):
        """ Gets the Revision from the Fan Controller Chip (should be 0x80) """
        rev= self.read_EMC2302(EMC2302_REVISION)
        return rev[0]

    def fan_status(self):
        """ Get the Fan Status
             The Fan Status register (0x24) indicates that one or both of the fan
             drivers has stalled or failed or that the Watchdog Timer has expired.
             Bits of interest are 7 (Watchdog), 2 (Drive), 1 (Spin) and 0 (Stall) """
        temp_data = self.read_EMC2302(FAN_STATUS)
        fanstatus = [0,0,0,0]
        fanstatus[0] = temp_data[0] & 1
        fanstatus[1] = temp_data[0] >> 1 & 1
        fanstatus[2] = temp_data[0] >> 2 & 1
        fanstatus[3] = temp_data[0] >> 7 & 1
        return fanstatus

    def fan_stall_status(self):
        """ Get the Fan Stall Status
             The Fan Stall Status register indicates which fan driver has detected
             a stalled condition. "1" = fault
             All bits are cleared upon a read if the error condition has been removed.
             Bits of interest are 1 (Fan 2) and 0 (Fan 1) """
        temp_data = self.read_EMC2302(FAN_STALL_STATUS)
        fanstallstatus = [0,0]
        fanstallstatus[0] = temp_data[0] & 1
        fanstallstatus[1] = temp_data[0] >> 1 & 1
        return fanstallstatus

    def fan_spin_status(self):
        """ Get the Fan Spin Status
             The Fan Stall Status register indicates which fan driver has failed
             to spin-up. "1" = fault
             All bits are cleared upon a read if the error condition has been removed.
             Bits of interest are 1 (Fan 2) and 0 (Fan 1) """
        temp_data = self.read_EMC2302(FAN_SPIN_STATUS)
        fanspinstatus = [0,0]
        fanspinstatus[0] = temp_data[0] & 1
        fanspinstatus[1] = temp_data[0] >> 2 & 1
        return fanspinstatus

    def fan_drive_fail_status(self):
        """ Get the Fan Drive Fail Status
             The Fan Stall Status register indicates which fan driver has detected
             a stalled condition. "1" = fault
             All bits are cleared upon a read if the error condition has been removed.
             Bits of interest are 1 (Fan 2) and 0 (Fan 1) """
        temp_data = self.read_EMC2302(DRIVE_FAIL_STATUS)
        fandrivestatus = [0,0]
        fandrivestatus[0] = temp_data[0] & 1
        fandrivestatus[1] = temp_data[0] >> 2 & 1
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
        temp_data = self.read_EMC2302(FAN_1_TACH_READ_LOW)
        fanrpm[0] = temp_data[0]
        temp_data = self.read_EMC2302(FAN_1_TACH_READ_HIGH)
        fanrpm[1] = temp_data[0]
        temp_data = self.read_EMC2302(FAN_2_TACH_READ_LOW)
        fanrpm[2] = temp_data[0]
        temp_data = self.read_EMC2302(FAN_2_TACH_READ_HIGH)
        fanrpm[3] = temp_data[0]
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
               * 0 - CLK Source - 0 (def): internal, 1: external """
        configregister = self.read_EMC2302(CONFIG_REGISTER)
        return configregister[0]

    def set_watchdog_continuous(self):
        """ Set the watchdog status bit (5) of the Configuration Register (0x20) to
             1 to enable continuous mode for the watchdog timer.
             In Continuous Operation, the Watchdog timer will start immediately.
             The timer will be reset by any access (read or write) to the SMBus
             register set. The four second Watchdog timer will restart upon
             completion of SMBus activity. """
        configregister = self.read_EMC2302(CONFIG_REGISTER)
        newconfigregister = configregister[0] | 32
        self.write_EMC2302(CONFIG_REGISTER,newconfigregister)
        checkconfigregister = self.read_EMC2302(CONFIG_REGISTER)
        watchdog = checkconfigregister[0] >> 5 & 1
        return watchdog

    def set_fan_range_bits(self):
        """ Set the Fan Range bits for Tacho multiplier
             Bits 6 & 5 of the Fan Configuration Registers (0x32 & 0x42) adjusts
             the range of reported and programmed tachometer reading values.
             The RANGE bits determine the weighting of all TACH values (including
             the Valid TACH Count, TACH Target, and TACH reading).

             0-0 = x 1 (500 min RPM)
             0-1 = x 2 (1000 min RPM) *DEFAULT
             1-0 = x 4 (2000 min RPM)
             1-1 = x 8 (4000 min RPM)

             We want 0-0 as need to measure down to approx 400 RPM
        """
        fanconfigregister = self.read_EMC2302(FAN_2_CONFIG1)
        print("fan register = ", fanconfigregister[0], " (", bin(fanconfigregister[0]), ")")
        newfanconfigregister = fanconfigregister[0] & 0b10011111
        print("new fan register = ", newfanconfigregister, " (", bin(newfanconfigregister), ")")
        self.write_EMC2302(FAN_2_CONFIG1,newfanconfigregister)
        checkfanconfigregister = self.read_EMC2302(FAN_2_CONFIG1)
        fanrange = checkfanconfigregister[0] & 0b01100000
        print("fan range = ", fanrange, " (", bin(fanrange), ")")
        return fanrange



