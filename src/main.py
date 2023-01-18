from machine import Pin
from umqtt.simple import MQTTClient
import json
import network
import sys
import time
import uasyncio.core as uasyncio

wlan = network.WLAN(network.STA_IF)
door_sensor = Pin(15, Pin.IN, Pin.PULL_UP)
led =  Pin("LED", Pin.OUT)
relay = Pin(21, Pin.OUT)

while not wlan.isconnected():
    print('waiting to connect')

led.value(1)

UNIQUE_CLIENT_ID = 'garage_door'
TOPIC_SUB = bytes('ha/garage/garage_door/set','utf-8')
TOPIC_PUB = bytes('ha/garage/garage_door/state','utf-8')

def callback(topic, msg):
    """mqtt callback"""
    message = msg.decode().strip("'\n")
    print(message)
    print((topic, msg))
    relay.toggle()
    time.sleep(0.5)
    relay.toggle()
    time.sleep(0.5)

client = MQTTClient(client_id = UNIQUE_CLIENT_ID,
    server = {{ HA_SERVER }},
    user = {{ HA_USERNAME }},
    password = {{ HA_PASSWORD }},
    ssl = False)
try:
    client.set_callback(callback)
    client.connect()
    client.subscribe(TOPIC_SUB)
except Exception as e:
    sys.print_exception(e)

async def publish_door_state(topic_pub):
    while True:
        if door_sensor.value() == 1:
            door_state = 'closed'
        else:
            door_state = 'open'
        data = {
            'door_state': door_state
        }
        json_data = json.dumps(data)
        msg = bytes(json_data, 'utf-8')
        client.publish(topic_pub, msg, )
        print(f'publishing: [{msg}]')
        await uasyncio.sleep(5)

async def main():
    
    uasyncio.create_task(publish_door_state(TOPIC_PUB))
    
    while True:
        try:
            client.check_msg()
            await uasyncio.sleep(0.5)
        except Exception as e:
            sys.print_exception(e)
            client.disconnect()

uasyncio.run(main())
