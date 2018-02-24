#This file gets the temperature from the pysense board from the Si7006-A20 chip.

##############################
# Libraries
##############################
from machine import I2C
from machine import Pin
import time

##############################
# Variables
##############################
scl_pi=26
sda_pin=25
temp_addr=41
measure_humidity = 0xF5
measure_temp = 0xF3
read_temp = 0xE0
result = bytearray(2)

##############################
# Configurations
##############################
i2c = I2C(scl=Pin(scl_pi), sda=Pin(sda_pin))


##############################
# Subroutines
##############################
def _getWord(high, low):
    return ((high & 0xFF) << 8) + (low & 0xFF)

##############################
# Main
##############################

# Scan i2c bus
addresses_found = i2c.scan()
print('Found the following devices')
print(addresses_found)

# Get Firmware Version
i2c.writeto(temp_addr, bytearray([0x84])+ bytearray([0xB8]))
time.sleep(0.5)
fw = i2c.readfrom(temp_addr, 1)
print('Firmware = ')
print(fw)

# Read Humidity
print('Requesting Humididty Measurement...')
i2c.writeto(temp_addr, bytearray([measure_humidity]))
time.sleep(1)
result = i2c.readfrom(temp_addr, 3)
result = _getWord(result[0], result[1])
print('Humidity = ')
print(result)

# Read Temperature
print('Requesting Temperature Measurement...')
i2c.writeto(temp_addr, bytearray([measure_temp]))
time.sleep(1)
result = i2c.readfrom(temp_addr, 3)
print('Temp = ')
print(result)
print('Requesting Temperature Result...')
i2c.writeto(temp_addr, bytearray([read_temp]))
result = i2c.readfrom(temp_addr, 3)
print('Temp2 = ')
print(result)



