#This file gets the temperature from the pysense board from the Si7006-A20 chip.

from machine import I2C
from machine import Pin
import time

i2c = I2C()
