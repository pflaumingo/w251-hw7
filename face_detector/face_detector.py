import sys
import os
import urllib
import tensorflow.contrib.tensorrt as trt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow as tf
import numpy as np
import time
from tf_trt_models.detection import download_detection_model, build_detection_graph
import cv2 as cv
import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="broker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="facial_images"

FROZEN_GRAPH_NAME = 'data/frozen_inference_graph_face.pb'
# !wget https://github.com/yeephycho/tensorflow-face-detection/blob/master/model/frozen_inference_graph_face.pb?raw=true -O {FROZEN_GRAPH_NAME}

output_dir=''
frozen_graph = tf.GraphDef()
with open(os.path.join(output_dir, FROZEN_GRAPH_NAME), 'rb') as f:
    frozen_graph.ParseFromString(f.read())

INPUT_NAME='image_tensor'
BOXES_NAME='detection_boxes'
CLASSES_NAME='detection_classes'
SCORES_NAME='detection_scores'
MASKS_NAME='detection_masks'
NUM_DETECTIONS_NAME='num_detections'

input_names = [INPUT_NAME]
output_names = [BOXES_NAME, CLASSES_NAME, SCORES_NAME, NUM_DETECTIONS_NAME]

tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = True

tf_sess = tf.Session(config=tf_config)
tf.import_graph_def(frozen_graph, name='')

tf_input = tf_sess.graph.get_tensor_by_name(input_names[0] + ':0')
tf_scores = tf_sess.graph.get_tensor_by_name('detection_scores:0')
tf_boxes = tf_sess.graph.get_tensor_by_name('detection_boxes:0')
tf_classes = tf_sess.graph.get_tensor_by_name('detection_classes:0')
tf_num_detections = tf_sess.graph.get_tensor_by_name('num_detections:0')
DETECTION_THRESHOLD = 0.5

class FaceDetector:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
    
    def process(self):
        cap = cv.VideoCapture(1)

        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            image_resized = cv.resize(frame, (300, 300))

            # We don't use the color information, so might as well save space
            scores, boxes, classes, num_detections = tf_sess.run([tf_scores, tf_boxes, tf_classes, tf_num_detections], feed_dict={
                tf_input: image_resized[None, ...]
            })

            boxes = boxes[0] # index by 0 to remove batch dimension
            scores = scores[0]
            classes = classes[0]
            num_detections = num_detections[0]

            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            for i in range(int(num_detections)):
                if scores[i] < DETECTION_THRESHOLD:
                    continue
                
                box = boxes[i] * np.array([gray.shape[0], gray.shape[1], gray.shape[0], gray.shape[1]])
                # print(box)
                face = gray[int(box[0]):int(box[2]), int(box[1]):int(box[3])]
                cv.imshow('frame', face)#face)
                rc, png = cv.imencode('.png', face)
                message = png.tobytes()
                self.mqtt_client.publish(LOCAL_MQTT_TOPIC, message)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break


def on_connect(client, userdata, flags, rc):
    print("Connected facial image publisher to local broker with rc: " + str(rc))


def on_publish(client, userdata, mid):
    print("A face has just been published")



local_mqtt_client = mqtt.Client()
local_mqtt_client.on_connect = on_connect
local_mqtt_client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

face_detector = FaceDetector(local_mqtt_client)
face_detector.process()

