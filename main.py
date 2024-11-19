from machine import Pin, I2C
from bmp280 import *
from time import sleep
import network
import socket
import machine
import config

#network
ssid = config.ssid
password = config.password

#connection
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Odottaa yhteyttä")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

#busss
i2c = I2C(0, scl=Pin(1), sda=Pin(0))	


bmp = BMP280(i2c, addr=0x76, use_case=BMP280_CASE_HANDHELD_DYN)


def send_data(data):
    address = socket.getaddrinfo(config.server, config.port)[0][-1]
    s = socket.socket()
    s.connect(address)
    s.send(data)
    s.close()

ip = connect()

while True:
    temperature = bmp.temperature   
    pressure = bmp.pressure

    print("Temperature: {:.2f} °C".format(temperature))
    print("Pressure: {:.2f} hPa".format(pressure))

    sleep(1)