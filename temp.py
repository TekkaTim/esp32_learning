#This file gets the temperature from the pysense board from the Si7006-A20 chip.

from machine import I2C
from machine import Pin
import time

scl_pi=26
sda_pin=25

i2c = I2C(scl=Pin(scl_pi), sda=Pin(sda_pin))

# Scan i2c bus
addresses_found = i2c.scan()
print(addresses_found)


