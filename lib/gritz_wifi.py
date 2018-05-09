##########################
# Subroutines
##########################

__version__ = '0.0.1'

def WLAN_Connect(the_ssid):
    from network import WLAN
    import machine
    from time import sleep
    ssid_found=0
    ssid_connected=0
    print('Attempting to connect to '+the_ssid+'....')
    wlan = WLAN(mode=WLAN.STA)
    nets = wlan.scan()
    #print("SSIDs found = "+nets)               # for debugging
    for net in nets:
        #print("Trying ",+net)                  # for debugging
        if net.ssid == the_ssid:
            ssid_found=1
            retries=0
            print('Network found!')
            wlan.connect(net.ssid, auth=(WLAN.WPA2, 'something_tricky!'), timeout=1000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting
                #print('WLAN connection not connected yet..')   # for debugging
                retries+=1
                if retries >= 20: break
            ssid_connected=wlan.isconnected()
    if ssid_connected == 1:
        print('WLAN connection succeeded. Getting WLAN information...')
        #print("Connected to "+net_to_use+" with IP address:" + wl.ifconfig()[0])
        ip_addr=wlan.ifconfig()[0]
        retries=0
        while (ip_addr == '0.0.0.0'):
            machine.idle() # save power while waiting
            ip_addr=wlan.ifconfig()[0]
            retries+=1
            if retries >= 20: break
        #print(wlan.ifconfig())                 # for debugging
        if ip_addr != '0.0.0.0':
            print('IP Address = '+ip_addr)
        else:
            print('Failed to get IP Address!')
    else:
        print('WLAN connection FAILED!')
