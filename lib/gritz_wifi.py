##########################
# Subroutines
##########################

__version__ = '0.0.1'

def WLAN_Connect(the_ssid):
    from network import WLAN
    import machine
    from time import sleep
    print("Attempting to connect to "+the_ssid+"....")
    wlan = WLAN(mode=WLAN.STA)
    nets = wlan.scan()
    #print("SSIDs found = "+nets)
    for net in nets:
        #print("Trying ",+net)
        if net.ssid == the_ssid:
            print('Network found!')
            wlan.connect(net.ssid, auth=(WLAN.WPA2, 'something_tricky!'), timeout=1000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting
                print('WLAN connection failed!')
            print('WLAN connection succeeded!')
            break
    #print("Connected to "+net_to_use+" with IP address:" + wl.ifconfig()[0])
    print('Getting WLAN information...')
    ip_addr=wlan.ifconfig()[0]
    while (ip_addr == '0.0.0.0'):
        machine.idle() # save power while waiting
        ip_addr=wlan.ifconfig()[0]
    #print(wlan.ifconfig())
    print("IP Address = "+ip_addr)
