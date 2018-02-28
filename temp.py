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
temp_addr = const(0x40)
measure_humidity = const(0xF5)
measure_temp = const(0xF3)
read_temp = const(0xE0)
#result = bytearray(2)

##############################
# Configurations
##############################
i2c = I2C(scl=Pin(scl_pi), sda=Pin(sda_pin))


##############################
# Subroutines
##############################
#def _getWord(high, low):
#    return ((high & 0xFF) << 8) + (low & 0xFF)

##############################
# Main
##############################

# Scan i2c bus
addresses_found = i2c.scan()
print('Found the following devices')
print(addresses_found)

for x in range(25):
  # Get Firmware Version
  i2c.writeto(temp_addr, bytearray([0x84])+ bytearray([0xB8]))
  time.sleep(0.1)
  fw = i2c.readfrom(temp_addr, 1)
  print('Firmware = ')
  print(fw[0])
  time.sleep(1)

 ## Read Humidity
 # print('Requesting Measurement...')
 # #i2c.writeto(temp_addr, bytearray(measure_humidity))
 # i2c.writeto(temp_addr, bytearray([0xF5]))
 # time.sleep(0.5)
 # #print('Getting Humidity...')
 # hum = i2c.readfrom(temp_addr, 2)
 # print('Humidity = ')
 # print(hum[0])


# this is erroring saing that there is no device when doing humidity, but the code works for firmware
#  so there shouldn't be any issue. it might be that the sensor is not ready in time, OR the data has
#  gone stale by the time I request it.  Sometimes this code works.... I have tried 0.5, 1 and 1.5 
#  second delays and it doesn't make much difference. FYI firmware ALWAYS works.


  # Read Temperature
  print('Requesting Temperature Measurement...')
  #i2c.writeto(temp_addr, bytearray(measure_temp))
  i2c.writeto(temp_addr, bytearray([0xF3]))
  time.sleep(1)
  print('Getting Temperature...')
  temp_result = i2c.readfrom(temp_addr, 3)
  print('Temp = ')
  print(result)

  print('Getting Temperature...')
  i2c.writeto(temp_addr, bytearray([read_temp]))
  result = i2c.readfrom(temp_addr, 3)
  print('Temp2 = ')
  print(result)



