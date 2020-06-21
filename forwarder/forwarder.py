import paho.mqtt.client as mqtt
import sys

# REMOTE_MQTT_HOST="52.116.42.249"
# REMOTE_MQTT_PORT=1883
# REMOTE_MQTT_TOPIC="remote_facial_images"

# def on_connect_remote(client, userdata, flags, rc):
#     print("connected to the local broker:" + str(rc))

# remote_mqtt_client = mqtt.Client()
# remote_mqtt_client.on_connect = on_connect_remote
# remote_mqtt_client.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)

LOCAL_MQTT_HOST="broker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="facial_images"

def on_connect(client, userdata, flags, rc):
    print("connected to the local broker:" + str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        print("message received")
        # remote_mqtt_client.publish(REMOTE_MQTT_TOPIC, payload=msg.payload, qos=0, retain=False)
    except:
        print("Unexpected error:", sys.exc_info()[0])


local_mqtt_client = mqtt.Client()
local_mqtt_client.on_connect = on_connect
local_mqtt_client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqtt_client.on_message = on_message

local_mqtt_client.loop_forever()