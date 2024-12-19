from machine import Pin, I2C
from bmp280 import *
from time import sleep
import network
import socket
import machine
import config.config
import requests
import json


#network
ssid = config.config.ssid
password = config.config.password

#busss
i2c = I2C(0, scl=Pin(1), sda=Pin(0))


bmp = BMP280(i2c, addr=0x76, use_case=BMP280_CASE_HANDHELD_DYN)


#connect

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while True:
    if wlan.status() == 3: # connected
        print('[INFO] CONNECTED!')
        network_info = wlan.ifconfig()
        print('[INFO] IP address:', network_info[0])
        break
    print('Waiting for Wi-Fi connection...')
    sleep(1)
        

address = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(address)
s.listen(1)
print('Kuunnellaan: ', address)




while True:

    temperature = bmp.temperature
    
    
    print(temperature)
    
    
    
    data = {"temp": temperature}
    
    url = "http://130.231.14.3:5000/temperature"
    print(json.dumps(data))
    response = requests.post(url, data=json.dumps(data))
    print(response)
    print(response.content)
    print(response.text)

    response.close()

    sleep(3)
    
