# -*- coding: utf-8 -*-
import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import random
from xbee import XBee,ZigBee
import serial 
import time
import io
from twilio.rest import Client
import os


#  Account SID from twilio.com/console
account_sid = "AC93c9b91ac681638840113c1fa0b0eeec"
#  Auth Token from twilio.com/console
auth_token  = "6934e7043aeacb7799377da36ddce96a"
# twilio client
client_tw = Client(account_sid, auth_token)


#Serial Port xbee 
port='/dev/ttyUSB0'
ser = serial.Serial(port, 9600, timeout=1)  # Le port utilis� /dev/ttyUSB0
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
xbee= ZigBee(ser)
#@ip platform thingsboard 
THINGSBOARD_HOST = '192.168.43.213'
# acces token device 
ACCESS_TOKEN = 'TokenRaspTemp1452'
# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'temperature': 0,'motion':False}
next_reading = time.time() 
#creation of mqtt client
client = mqtt.Client()
send_sms=0
# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to Thingsboard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()
send_smssend_sms=False
try:
    while True:
        
        temperature =(dict(xbee.wait_read_frame()['samples'][0])['adc-2']*1200/1024)/10
      
        print(temperature)
        sensor_data['temperature'] = temperature
        if(temperature>=40 and send_sms==0):
            send_sms+=1
            message = client_tw.messages.create(to="+21658968508", from_="+12058815147",body="Warning,temperture is higher than 40 ")
                
        
        motion=dict(xbee.wait_read_frame()['samples'][0])['dio-3']
        print("{:g}\u00b0C".format(motion))
        sensor_data['motion']=motion
      
        
        #sensor_data['motion'] = dict(xbee1.wait_read_frame()['samples'][0])['dio-3']

        # Sending MOTION and temperature data to Thingsboard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(10)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
xbee.halt()
ser.close()
