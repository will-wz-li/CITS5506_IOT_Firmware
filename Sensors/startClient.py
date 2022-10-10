from rpiSensors import Sensor
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep
import random
import sys

#IP Address or Hostname of the Webserver
hostname = ''.join(sys.argv[1:2])
#IP Address or Hostname of the Webserver
carpark = ''.join(sys.argv[2:3])
#A list of parking bay IDs being measured
idList = list(sys.argv[3:])

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/carpark")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(host=hostname, port=1883, keepalive=60)

# Map Each ID to a Sensor
firstSensor = Sensor(idList[0], 0, {"PIN_TRIGGER": 4, "PIN_ECHO": 17}, {"PIN_LED": 27})
SensorList = []
SensorList.append(firstSensor)

try:
    while(True):
        for sensor in SensorList:
            binarystatus = sensor.getStatus()
            if(binarystatus == 1):
                status = "full"
            else:
                status = "empty"
            parkingbay = {
                "status": status, # change
                "carpark": carpark, # change
                "id": sensor.id,
            }
            client.publish("/carpark", str(parkingbay))

        #Refreshes MQTT connection
        client.loop()
except KeyboardInterrupt:
    print("Stopped")
    GPIO.cleanup()