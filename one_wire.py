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
watchdog=tim.set_watchdog_continuous()
fanrange=tim.set_fan_range_bits()
if ( watchdog == 1 ):
  print("EMC2302 WatchDog Timer Set to Continuous")
  #check alert?
else:
  print("EMC2302 WatchDog Timer Set to Single Shot! Check Config!")


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
# Get EMC2302 Chip Info
#########################################

# Get Manufacturer Information from Fan Controller Chip
print("Reading Fan Controller Chip Info...")
data=tim.product_id()
print("Product ID =",data," ("+hex(data)+")")
data=tim.manufacturer_id()
print("Manufacturer ID =",data," ("+hex(data)+")")
data=tim.revision()
print("Revision =",data," ("+hex(data)+")")

# Get Config Register Setting
print("Reading Configuration Register...")
data=tim.get_config_register()
print("Configuration Register =",data," ("+hex(data)+")")

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
        time.sleep_ms(50)
      read_count=0
      for ts in temp_sensors:
        read_count += temp_sensors[ts]["read"]
      if ( read_count >= num_devices ):
        all_temp_done = 1

  # Print out the Temperatures
  print("\nTemperatures are...")
  for key in temp_sensors:
    if (temp_sensors[key]["available"] == 1):
      print("Temp", key, " = ",temp_sensors[key]["celcius"])
      temp_sensors[key]["read"]=0


  #########################################
  # GET FAN DATA
  #########################################

  # Get Fan Status
  print("\nGetting Fan Status...")
  fan_status=tim.fan_status()
  fan_stall_status=tim.fan_stall_status()
  fan_spin_status=tim.fan_spin_status()
  fan_drive_fail_status=tim.fan_drive_fail_status()
  print("====================================")
  print("| Item     | Total | Fan 1 | Fan 2 |")
  print("| Stall    |  ",fan_status[0],"  |  ",fan_stall_status[0],"  |  ",fan_stall_status[1],"  |")
  print("| Spin     |  ",fan_status[1],"  |  ",fan_spin_status[0],"  |  ",fan_spin_status[1],"  |")
  print("| Drive    |  ",fan_status[2],"  |  ",fan_drive_fail_status[0],"  |  ",fan_drive_fail_status[1],"  |")
  print("| Watchdog |  ",fan_status[3],"  |   -   |   -   |")
  print("====================================")

  print("\nGetting Fan RPMs...")
  fan_rpm=tim.fan_rpm()
#  print("Fan 1 RPM High =    ", fan_rpm[1],", Fan 1 RPM Low =    ", fan_rpm[0])
#  print("Fan 2 RPM High =    ", fan_rpm[3],", Fan 2 RPM Low =    ", fan_rpm[2])
  print("Fan 2 RPM High =", fan_rpm[3], " ("+bin(fan_rpm[3])+"), Fan 2 RPM Low =", fan_rpm[2], " ("+bin(fan_rpm[2])+")")

  fan2_rpm_count = (fan_rpm[3] << 8) + fan_rpm[2]
  fan2_rpm_count = fan2_rpm_count >> 3
  fan2_rpm = 3932160 / fan2_rpm_count
  #fan2_rpm = 7864320 / fan2_rpm_count

  print("Fan 2 RPM =",fan2_rpm)

  time.sleep(1)
  # ASSESS TEMPERATURE VS FAN DATA
  #  rpm_rate_required=0
  #  for key in temp_sensors:
  #    for rate in fan_rpm_speeds

