#This file gets the temperature from the pysense board from the Si7006-A20 chip.

from machine import I2C
from machine import Pin
import time

i2c = I2C(scl=Pin(13), sda=Pin(12))
bob = i2c.scan()
print(bob)
#i2c = I2C(scl=Pin(5), sda=Pin(4))
