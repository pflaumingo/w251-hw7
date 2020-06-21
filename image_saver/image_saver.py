# img = cv.imread('/home/noah/Downloads/hw03.png', -1)
# # cv.imshow('image', img)
# # cv.waitKey(0)
# rc, png = cv.imencode('.png', img)
# f = open('/bucket_of_faces/hw03_encoded.png', 'wb')
# f.write(png.tobytes())
# f.close()

import paho.mqtt.client as mqtt
import sys

REMOTE_MQTT_HOST="remote-broker"
REMOTE_MQTT_PORT=1883
REMOTE_MQTT_TOPIC="remote_facial_images"


def on_connect(client, userdata, flags, rc):
    print("connected to the local broker:" + str(rc))
    client.subscribe(REMOTE_MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        f = open('/bucket_of_faces/' + str(msg.timestamp) + '.png', 'wb')
        f.write(msg.payload)
        f.close()
    except:
        print("Unexpected error:", sys.exc_info()[0])


local_mqtt_client = mqtt.Client()
local_mqtt_client.on_connect = on_connect
local_mqtt_client.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)
local_mqtt_client.on_message = on_message

local_mqtt_client.loop_forever()