from PIL import Image
import sys
import os
import urllib
# import tensorflow.contrib.tensorrt as trt
from tensorflow.python.compiler.tensorrt import trt_convert as trt
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#import matplotlib.patches as patches
import tensorflow as tf
import numpy as np
import time
# from tf_trt_models.tf_trt_models.detection import download_detection_model, build_detection_graph

IMAGE_PATH = 'data/warriors.jpg'
FROZEN_GRAPH_NAME = 'data/frozen_inference_graph_face.pb'


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

trt_graph = trt.create_inference_graph(
    input_graph_def=frozen_graph,
    outputs=output_names,
    max_batch_size=1,
    max_workspace_size_bytes=1 << 25,
    precision_mode='FP16',
    minimum_segment_size=50
)