from pysense import Pysense
from SI7006A20 import SI7006A20
from machine import I2C
from machine import Pin
import time

py = Pysense()
si = SI7006A20(py)

for x in range(25):
  print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
  print("Dew point: "+ str(si.dew_point()) + " deg C")
  t_ambient = 24.4
  print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")
