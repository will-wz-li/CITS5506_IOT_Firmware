importpaho.mqtt.clientasmqtt

fromtimeimportsleep

importrandom

importjson


defon_connect(client, userdata, flags, rc):

print("Connected with result code "+str(rc))

client.subscribe("/carpark")


defon_message(client, userdata, msg):

print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message

client.connect(host="127.0.0.1", port=1883, keepalive=60)


while(True):

parkingbayid = random.randint(1,6)

status = random.randint(0,1)

data = {

"status": "empty"ifstatus == 0else"full",

"carpark": "uwacarpark1",

"id": parkingbayid,

    }

client.publish("/carpark", json.dumps(data))

client.loop(10)