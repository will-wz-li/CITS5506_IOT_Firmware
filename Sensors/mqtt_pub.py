import paho.mqtt.client as mqtt
from time import sleep
import random


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.ws_set_options(client, path="/carpark", headers=None)
client.connect(host="192.168.137.1", port=1883, keepalive=60)

#client.publish("/carpark", data2)



while(True):
    data2 = {
        "status": "full",
        "carpark": "carpark",
        "id": random.randint(1,69),
    }
    data3 = {
        "status": "empty",
        "carpark": "carpark",
        "id": random.randint(1,69),
    }

    client.publish("/carpark", str(data2))
    client.publish("/carpark", str(data3))

    sleep(1)
    client.loop()