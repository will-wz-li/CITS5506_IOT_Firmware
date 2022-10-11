from rpiSensors import Sensor
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep
from socket import *
import json
import sys

#IP Address or Hostname of the Webserver
hostname = ''.join(sys.argv[1:2])
#Name of carpark on webserver
carpark = ''.join(sys.argv[2:3])
#A list of parking bay IDs being measured
idList = []
numBays = int(sys.argv[3:][0])

# Determines if the MQTT instance is currently connected
flag_connected = 0


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/carpark")
    global flag_connected
    flag_connected = 1

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code "+str(rc))
    global flag_connected
    flag_connected = 0

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(host=hostname, port=1883, keepalive=60)

# Map Each ID to a Sensor
for i in range(numBays):
    idList.append(i+1)

print(len(idList))
firstSensor = Sensor(idList[0], {"BUS": 1}, {"PIN_TRIGGER": 4, "PIN_ECHO": 14}, {"GREEN_LED": 15, "RED_LED": 18})

secondSensor = Sensor(idList[1], {"BUS": 4}, {"PIN_TRIGGER": 5, "PIN_ECHO": 6}, {"GREEN_LED": 10, "RED_LED": 9})

thirdSensor = Sensor(idList[2], {"BUS": 3}, {"PIN_TRIGGER": 21, "PIN_ECHO": 20}, {"GREEN_LED": 16, "RED_LED": 19})

SensorList = []
SensorList.append(firstSensor)
SensorList.append(secondSensor)
SensorList.append(thirdSensor)


try:
    while(True):
        if(flag_connected == 0):
            print(f"Attempting to connect to {hostname}")
            try:
                client.connect(host=hostname, port=1883, keepalive=60)
            except timeout:
                print("Connection timeout")
        for sensor in SensorList:
            binarystatus = sensor.getStatus()
            if(binarystatus == 1):
                status = "full"
            else:
                status = "empty"
            parkingbay = {
                "status": status,
                "carpark": carpark,
                "id": sensor.id,
            }
            client.publish("/carpark", json.dumps(parkingbay))
        #Refreshes MQTT connection
        client.loop(0.1)
except KeyboardInterrupt:
    print("Stopped")
    GPIO.cleanup()
