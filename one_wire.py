import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire

#DS18B20 data line connected to pin P10
ow = OneWire(Pin('P10'))
temp = DS18X20(ow)
print('Scanning the One Wire Bus....')
devices = ow.scan()
num_devices=len(devices)
device_read=[0] * num_devices
temperatures=[0] * num_devices

print('The following devices have been found....')
for device in devices:
  device_serial="".join("%02x" % device[c-1] for c in range(len(device), 0, -1))
  print("  * Serial Number = ", device_serial)

print("Num Devices = ", num_devices)
temp_retry=0

#while True:
for x in range(1):
  temp_not_done=1
  for device in devices:
    temp.start_convertion(device)
    time.sleep_ms(10)

  while True:
    temp_retry+=1
    if ( temp_retry > 20 ):
      break
    print("Retry = ", temp_retry)
    for i in range(0,num_devices):
      if (device_read[i]!= 1):
        temp_data = (temp.read_temp_async(devices[i]))
        print("temp_data #", i, " = ", temp_data)
        if (temp_data != None):
          print("here")
          temperatures[i] = temp_data
          device_read[i] = 1
      time.sleep_ms(100)
    if ( sum(device_read) == num_devices ):
      break


  #device_read=[0] * num_devices


# isbusy()???
#    time.sleep_ms(1000)




#temp.start_convertion()
#time.sleep(1)

#while True:
#    print(temp.read_temp_async())
#    time.sleep(1)
#    temp.start_convertion()
#    time.sleep(1)
