import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire

__version__ = '0.0.1'

class NASTemp:
    """ This is to read the temperatures of the DS18B20 Temperature
        sensors in the NAS environment.
        Uses the Pycom onewire library.
    """

    def __init__(self, owpin='P10'):
        #DS18B20 data line connected to pin P10
        ow=OneWire(Pin(owpin))
        nastemp = DS18X20(ow)


    #def get_devices(self)
        #devices = ow.scan()
        #return devices

    
    #def (self, devices)
        #num_devices_found=len(devices)
        #for key in devices:
        #    device_serial="".join("%02x" % key[c-1] for c in range(len(key), 0, -1))
        #    print("  * ",device_serial)
        #return ??

#    def convert_serial(self,serial_le)
#        serial_string="".join("%02x" % serial_le[c-1] for c in range(len(serial_le[*]), 0, -1))
#                     "".join("%02x" % temp_sers[c-1] for c in range(len(temp_ors]), 0, -1))
#        return serial_string

