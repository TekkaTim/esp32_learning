import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire

#DS18B20 data line connected to pin P10
ow = OneWire(Pin('P10'))
temp = DS18X20(ow)

result=OneWire.scan(ow)
print(result)
temp.start_convertion()
time.sleep(1)

while True:
    print(temp.read_temp_async())
    time.sleep(1)
    temp.start_convertion()
    time.sleep(1)
