import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire

#DS18B20 data line connected to pin P10
ow = OneWire(Pin('P10'))
temp = DS18X20(ow)

#ds = DS18X20(OneWire(Pin('P10')))
#print('devices:', ds.roms)
##devices: [bytearray(b'(\xff\xae8\x90\x15\x03T')]
#print('temperatures:', ds.read_temps())
##temperatures: [2525]


devices = ow.scan()
#roms = ds.scan()
print('found probes:', devices)
#print('found probes:', roms)
 
while True:
    print('temperatures:', end=' ')
    #ow.convert_temp()  
    for device in devices:
        temp.start_convertion(device)
        time.sleep(1)
#        ow.select_rom(device)
#Doesnt really work for selection the sesnor, gives "bound_method" response :-(
        print(temp.read_temp_async, end=' ')
    print()
#    time.sleep_ms(1000)






#temp.start_convertion()
#time.sleep(1)

#while True:
#    print(temp.read_temp_async())
#    time.sleep(1)
#    temp.start_convertion()
#    time.sleep(1)
