'''
@Author: Aaron.chen
@Date: 2026-03-31
@LastEditTime: 2020-04-24 17:06:08
@Description: example for module umqtt
@FilePath: example_mqtt_file.py
'''
from umqtt import MQTTClient
import utime
import log
import checkNet
import audio
import ujson
from machine import Pin


state = 0
usrname="quectel"
password="12345678"

gpio1=Pin(Pin.GPIO31,Pin.OUT,Pin.PULL_DISABLE,1)

def sub_cb(topic, msg):
    data=msg.decode()
    print(data)
    if data ==  "led":
        gpio1.write(0)
        print("led open...")
        utime.sleep(3)
        gpio1.write(1)



if __name__ == '__main__':
    
    try:
        c = MQTTClient("umqtt_client", "101.37.104.185", 41094,usrname,password,ssl=True)
        c.set_callback(sub_cb)
        c.connect()
        c.subscribe("/public/TEST/python")
        c.publish("/public/TEST/python", "my name is Quecpython!")

        while True:
            c.wait_msg()
            utime.sleep(1)
    except KeyboardInterrupt as e:
        c.disconnect()

