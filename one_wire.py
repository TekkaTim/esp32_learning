import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire

#DS18B20 data line connected to pin P10
ow = OneWire(Pin('P10'))
temp = DS18X20(ow)

print('Scanning the One Wire Bus....')
devices = ow.scan()

print('The following devices have been found....')
for device_serial_array in devices:
  #hex_string="".join("%02x" %b for b in device_serial_array)
  #print(hex_string)
  device_serial="".join("%02x" % device_serial_array[c-1] for c in range(len(device_serial_array), 0, -1))
  print("  * Serial Number = ", device_serial)



#for number in devices
#    print(devices[number])

 
#while True:
#    print('temperatures:', end=' ')
#    #ow.convert_temp()
#    for device in devices:
#        temp.start_convertion(device)
#        time.sleep(1)
#        ow.select_rom(device)
##Doesnt really work for selection the sesnor, gives "bound_method" response :-(
#        print(temp.read_temp_async, end=' ')
#    print()
#    time.sleep_ms(1000)






#temp.start_convertion()
#time.sleep(1)

#while True:
#    print(temp.read_temp_async())
#    time.sleep(1)
#    temp.start_convertion()
#    time.sleep(1)
