import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire
from temperature import Calc_Temp
from gritz_wifi import WLAN_Connect
from machine import I2C
from NAS_Temp import NASTemp
from EMC2302 import EMC2302

#Connect to Wi-Fi
WLAN_Connect('gritz')

#DS18B20 data line connected to pin P10
ow = OneWire(Pin('P10'))
temp = DS18X20(ow)

# Initialize I2C for EMC2302
tim=EMC2302()

# Set Up Dictionary for Temperature Sensors.
temp_sensors = { "Intake" : { "serial" : bytearray(b'\x28\x89\x74\x29\x07\x00\x00\x89'),
                             "available" : 0,
                             "celcius" : 0,
                             "read" : 0 },
                 "HDD1"  : { "serial" : bytearray(b'\x28\xfe\x5a\x29\x07\x00\x00\xce'),
                             "available" : 0,
                             "celcius" : 0,
                             "read" : 0 },
#                 "HDD2"  : { "serial" : bytearray(b'\x28\xb3\x31\x29\x07\x00\x00\x90'),
#                             "available" : 0,
#                             "celcius" : 0,
#                             "read" : 0 },
#                 "Hot_Isle" : { "serial" : bytearray(b'\x28\xb3\x31\x29\x07\x00\x00\x90'),
#                             "available" : 0,
#                             "celcius" : 0,
#                             "read" : 0 },
                 "Exhaust"  : { "serial" : bytearray(b'\x28\x5b\xca\x29\x07\x00\x00\xce'),
                             "available" : 0,
                             "celcius" : 0,
                             "read" : 0 }
               }

num_devices=len(temp_sensors)

#Dictionary for Fan RPM rate at certain temperatures.
fan_speed_vs_temp = { "Intake" : {
                        "very_low":15,"low":18,"medium":20,"high":23,"very_high":25,"extreme":28 },
                      "HDD1" : {
                        "very_low":20,"low":25,"medium":30,"high":35,"very_high":40,"extreme":45 },
#                      "HDD2" : {
#                        "very_low":20,"low":25,"medium":30,"high":35,"very_high":40,"extreme":45 },
#                      "Hot_Isle" : {
#                        "very_low":20,"low":25,"medium":30,"high":35,"very_high":40,"extreme":45 },
                      "Exhaust" : {
                        "very_low":20,"low":25,"medium":30,"high":35,"very_high":40,"extreme":45 }
                    }
#Fan RPM Speeds.
fan_rpm_speeds = { "very_low":30, "low":40, "medium":50, "high":60, "very_high":80, "extreme":100 }

#########################################
# CHECK 1-WIRE BUS
#########################################

# Scan the 1-Wire bus and find available devices
print('Scanning the One Wire Bus....')
devices = ow.scan()
num_devices_found=len(devices)
#for key in devices:
#    device_serial="".join("%02x" % key[c-1] for c in range(len(key), 0, -1))
#    print("  * ",device_serial)

# Check to see if the sensors expected are available.
print('Looking for the following devices....')
for key in temp_sensors:
  sensor_found="Missing"
  if temp_sensors[key]["serial"] in devices:
    sensor_found="Available"
    temp_sensors[key]["available"]=1
  device_serial="".join("%02x" % temp_sensors[key]["serial"][c-1] for c in range(len(temp_sensors[key]["serial"]), 0, -1))
  #device_serial=NASTemp.convert_serial(temp_sensors[key]["serial"])
  print("  * "+key+" Serial Number = "+device_serial+" ("+sensor_found+")")


#########################################
# PUT IN A CHECK FOR NEW DEVICES
#########################################


#########################################
# GET TEMPERATURE DATA
#########################################

while True:
#for x in range(1):  # use this for testing
  # CHECK TEMPERATURE SENSORS
  temp_not_done=1
  temp_retry=0
  # Start Conversion process in Temp Sensors.
  for key in temp_sensors:
    if (temp_sensors[key]["available"] == 1):
      temp.start_convertion(temp_sensors[key]["serial"])
      time.sleep_ms(10)

  # Get temperature from sensors one by one until all are read.
  all_temp_done = 0
  for temp_retry in range(5):
    for key in temp_sensors:
      if (temp_retry >= 5) or (all_temp_done == 1):
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
      for ts in temp_sensors:
        read_count += temp_sensors[ts]["read"]
      if ( read_count >= num_devices ):
        all_temp_done = 1

  # Print out the Temperatures
  for key in temp_sensors:
    if (temp_sensors[key]["available"] == 1):
      print("Temp", key, " = ",temp_sensors[key]["celcius"])
      temp_sensors[key]["read"]=0


  #########################################
  # GET FAN DATA
  #########################################

  # Get Manufacturer Information from Fan Controller Chip
  print("Reading Fan Controller Chip Info...")
  data=tim.product_id()
  print("Product ID =",data[0]," ("+hex(data[0])+")")
  data=tim.manufacturer_id()
  print("Manufacturer ID =",data[0]," ("+hex(data[0])+")")
  data=tim.revision()
  print("Revision =",data[0]," (",hex(data[0]),")")

  # Get Fan Status
  print("Getting Fan Status...")
  data=tim.fan_status()
  print("Stall =", data[0])
  print("Spin =", data[1])
  print("Drive =", data[2])
  print("Watchdog =", data[3])

  # Get Fan Stall Status
  print("Getting Fan Stall Status...")
  data=tim.fan_stall_status()
  print("Stall Fan 1 =", data[0])
  print("Stall Fan 2 =", data[1])

  # Get Fan Spin Status
  print("Getting Fan Spin Status...")
  data=tim.fan_spin_status()
  print("Spin Fan 1 =", data[0])
  print("Spin Fan 2 =", data[1])

  # Get Fan Drive Fail Status
  print("Getting Fan Drive Fail Status...")
  data=tim.fan_drive_fail_status()
  print("Fan Drive Fail 1 =", data[0])
  print("Fan Drive Fail 2 =", data[1])

  # Get Fan RPM
  print("Getting Fan RPMs...")
  data=tim.fan_rpm()
  print("Fan 1 RPM High =", data[1])
  #data=tim.fan_rpm("2")
  print("Fan 1 RPM Low =", data[0])
  print("Fan 2 RPM High =", data[3])
  print("Fan 2 RPM Low =", data[2])

  # ASSESS TEMPERATURE VS FAN DATA
  #  rpm_rate_required=0
  #  for key in temp_sensors:
  #    for rate in fan_rpm_speeds

