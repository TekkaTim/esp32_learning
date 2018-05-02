import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire
from temperature import Calc_Temp
from gritz_wifi import WLAN_Connect
from machine import I2C

#Connect to Wi-Fi
WLAN_Connect('gritz')
#DS18B20 data line connected to pin P10
ow = OneWire(Pin('P10'))
temp = DS18X20(ow)
# I2C sda='P22' (G9), scl='P21' (G8)
SDA='P22'
SCL='P21'
i2c = I2C(0, I2C.MASTER, baudrate=20000, pins=(SDA,SCL))
i2c.init()
# THIS IS NOT FINDING ANYTHING ON THE I2C BUS. NEED 4.7Kohm?
# NEED TO TEST WITH THE DEFAULT
#i2c.deinit()
#fan_controller=i2c.scan()
print("Scanning I2C Bus...")
print("Found - ")
i2c.scan()
time.sleep(2)

temp_sensors = { "Intake" : { "serial" : bytearray(b'\x28\x89\x74\x29\x07\x00\x00\x89'),
                             "available" : 0,
                             "celcius" : 0,
                             "read" : 0 },
#                 "HDD1"  : { "serial" : bytearray(b'\x28\xb3\x31\x29\x07\x00\x00\x90'),
#                             "available" : 0,
#                             "celcius" : 0,
#                             "read" : 0 },
#                 "HDD2"  : { "serial" : bytearray(b'\x28\xb3\x31\x29\x07\x00\x00\x90'),
#                             "available" : 0,
#                             "celcius" : 0,
#                             "read" : 0 },
#                 "Hot_Isle" : { "serial" : bytearray(b'\x28\xb3\x31\x29\x07\x00\x00\x90'),
#                             "available" : 0,
#                             "celcius" : 0,
#                             "read" : 0 },
                 "Exhaust"  : { "serial" : bytearray(b'\x28\xb3\x31\x29\x07\x00\x00\x90'),
                             "available" : 0,
                             "celcius" : 0,
                             "read" : 0 }
               }

num_devices=len(temp_sensors)

#Fan RPM rate at certain temperatures.
fan_speed_vs_temp = { "Intake" : {
                        "very_low":15,"low":18,"medium":20,"high":23,"very_high":25,"extreme":28 },
#                      "HDD1" : {
#                        "very_low":20,"low":25,"medium":30,"high":35,"very_high":40,"extreme":45 },
#                      "HDD2" : {
#                        "very_low":20,"low":25,"medium":30,"high":35,"very_high":40,"extreme":45 },
#                      "Hot_Isle" : {
#                        "very_low":20,"low":25,"medium":30,"high":35,"very_high":40,"extreme":45 },
                      "Exhaust" : {
                        "very_low":20,"low":25,"medium":30,"high":35,"very_high":40,"extreme":45 }
                    }
#Fan RPM Speeds.
fan_rpm_speeds = { "very_low":30, "low":40, "medium":50, "high":60, "very_high":80, "extreme":100 }


print('Scanning the One Wire Bus....')
devices = ow.scan()
num_devices_found=len(devices)

print('Looking for the following devices....')
for key in temp_sensors:
  sensor_found="Missing"
  if temp_sensors[key]["serial"] in devices:
    sensor_found="Available"
    temp_sensors[key]["available"]=1
  device_serial="".join("%02x" % temp_sensors[key]["serial"][c-1] for c in range(len(temp_sensors[key]["serial"]), 0, -1))
  print("  * "+key+" Serial Number = "+device_serial+" ("+sensor_found+")")


# PUT IN A CHECK FOR NEW DEVICES

#for key in temp_sensors:
#  print(key, "temperature =", temp_sensors[key]["temperature"], ", read =", temp_sensors[key]["read"])

time.sleep(2)
while True:
#for x in range(1):
  # CHECK TEMPERATURE SENSORS
  temp_not_done=1
  temp_retry=0
  for key in temp_sensors:
    if (temp_sensors[key]["available"] == 1):
      temp.start_convertion(temp_sensors[key]["serial"])
      time.sleep_ms(10)

  #while True:
  for temp_retry in range(5):
    for key in temp_sensors:
      if ( temp_retry >= 4 ):
        print("Retries for sensor",key,"exceeded")
        break
      if (temp_sensors[key]["available"] == 1):
        if (temp_sensors[key]["read"] != 1):
          temp_data = (temp.read_temp_async(temp_sensors[key]["serial"]))
          if (temp_data != None):
            temp_data = Calc_Temp(temp_data)
            temp_sensors[key]["celcius"] = temp_data
            temp_sensors[key]["read"] = 1
        time.sleep_ms(100)
      read_count=0
      for key in temp_sensors:
        read_count += temp_sensors[key]["read"]
      if ( read_count >= num_devices ):
        break


  for key in temp_sensors:
    if (temp_sensors[key]["available"] == 1):
      print("Temp", key, " = ",temp_sensors[key]["celcius"])
      temp_sensors[key]["read"]=0



  # CHECK FAN DATA


  # ASSESS TEMPERATURE VS FAN DATA
#  rpm_rate_required=0
#  for key in temp_sensors:
#    for rate in fan_rpm_speeds

