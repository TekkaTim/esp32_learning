import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire
from temperature import Calc_Temp
from gritz_wifi import WLAN_Connect

#Connect to Wi-Fi
WLAN_Connect('gritz')
#DS18B20 data line connected to pin P10
ow = OneWire(Pin('P10'))
temp = DS18X20(ow)
temp_serials = {"Front" : bytearray(b'\x28\x89\x74\x29\x07\x00\x00\x89'),
                "Back"  : bytearray(b'\x28\xb3\x31\x29\x07\x00\x00\x90')}
num_devices=len(temp_serials)
temperature = { "Front" : 0,
                "Back"  : 0}
device_read = { "Front" : 0,
                "Back"  : 0}
temp_sensors = { "Front" : { "serial" : bytearray(b'\x28\x89\x74\x29\x07\x00\x00\x89'),
                             "available" : 0,
                             "temperature" : 22,
                             "read" : 33 },
                 "Back"  : { "serial" : bytearray(b'\x28\xb3\x31\x29\x07\x00\x00\x90'),
                             "available" : 0,
                             "temperature" : 44,
                             "read" : 55 } }

print('Scanning the One Wire Bus....')
devices = ow.scan()
num_devices_found=len(devices)


print('Looking for the following devices....')
for key in temp_serials:
  sensor_found="Missing"
  if temp_serials[key] in devices: sensor_found="Available"
  if temp_serials[key] in devices: temp_sensors[key]["available"]=1
  device_serial="".join("%02x" % temp_serials[key][c-1] for c in range(len(temp_serials[key]), 0, -1))
  print("  * ", key, " Serial Number = ", device_serial, " (",sensor_found,")")

# PUT IN A CHECK FOR NEW DEVICES

#for key in temp_sensors:
#  print(key, "temperature =", temp_sensors[key]["temperature"], ", read =", temp_sensors[key]["read"])

while True:
#for x in range(1):
  temp_not_done=1
  temp_retry=0
  for key in temp_serials:
    if (temp_sensors[key]["available"] == 1):
      temp.start_convertion(temp_serials[key])
      time.sleep_ms(10)

  while True:
    temp_retry+=1
    if ( temp_retry > 20 ):
      break
    for key in temp_serials:
      if (temp_sensors[key]["available"] == 1):
        if (device_read[key] != 1):
          temp_data = (temp.read_temp_async(temp_serials[key]))
          if (temp_data != None):
            temp_data = Calc_Temp(temp_data)
            temperature[key] = temp_data
            device_read[key] = 1
        time.sleep_ms(100)
    if ( sum(device_read.values()) == num_devices ):
      break
  for key in temperature:
    if (temp_sensors[key]["available"] == 1):
      print("Temp", key, " = ", temperature[key])
      device_read[key]=0

