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

print('The following devices have been found....')
for device in devices:
  device_serial="".join("%02x" % device[c-1] for c in range(len(device), 0, -1))
  print("  * Serial Number = ", device_serial)


while True:
  for device in devices:
    temp.start_convertion(device)
    time.sleep_ms(750)
    print(temp.read_temp_async(device))
    #time.sleep_ms(500)

#    time.sleep_ms(1000)






#temp.start_convertion()
#time.sleep(1)

#while True:
#    print(temp.read_temp_async())
#    time.sleep(1)
#    temp.start_convertion()
#    time.sleep(1)
