from styx_msgs.msg import TrafficLight

import numpy as np
import os
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf
from matplotlib import pyplot as plt
from PIL import Image
from os import path
from utils import label_map_util
from utils import visualization_utils as vis_util
import time
import cv2

##import functions.detect_red
##import functions.load_image_into_numpy_array
##import functions.read_traffic_lights


def detect_red(img, Threshold=0.01):
    """
    detect red and yellow
    :param img:
    :param Threshold:
    :return:
    """    
    desired_dim = (30, 90) # width, height
    img = cv2.resize(np.array(img), desired_dim, interpolation=cv2.INTER_LINEAR)
    img_hsv=cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # lower mask (0-10)
    lower_red = np.array([0,70,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170,70,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # red pixels' mask
    mask = mask0+mask1

    # Compare the percentage of red values
    rate = np.count_nonzero(mask) / (desired_dim[0] * desired_dim[1])

    if rate > Threshold:
        return True
    else:
        return False



def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


def read_traffic_lights(image, boxes, scores, classes, max_boxes_to_draw=20, min_score_thresh=0.5, traffic_ligth_label=10):
    im_height, im_width, _ = image.shape
    red_flag = False
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores[i] > min_score_thresh and classes[i] == traffic_ligth_label:
            ymin, xmin, ymax, xmax = tuple(boxes[i].tolist())
            (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                          ymin * im_height, ymax * im_height)
            top = np.int(np.floor(top))
            bottom = np.int(np.floor(bottom))
            left = np.int(np.floor(left))
            right = np.int(np.floor(right))

            crop_img = image[top:bottom, left:right, :]

            if detect_red(crop_img):
                red_flag = True

    return red_flag

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier

        # Path to frozen detection graph. This is the actual model that is used for the object detection.
        PATH_TO_CKPT = 'light_classification/faster_rcnn_resnet101_coco_11_06_2017' + '/frozen_inference_graph.pb'

        #--------Load a (frozen) Tensorflow model into memory
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        print('\n\n * * * * * SUCCESSFULLY LOADED THE GRAPH * * * * * \n\n')
        self.detection_graph = detection_graph

    
    def recognize(self):
        print('I recognize that I have light classification :)\n')


    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        print('\n\n About to classify an image \n\n')
        detection_graph = self.detection_graph

        with detection_graph.as_default():
            with tf.Session(graph=detection_graph) as sess:

                # Definite input and output Tensors for detection_graph
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
                detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
                detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                # the array based representation of the image will be used later in order to prepare the
                # result image with boxes and labels on it.

                ## since image is already numpy array, we remove this
                ## image_np = load_image_into_numpy_array(image)

                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                ## image_np_expanded = np.expand_dims(image_np, axis=0)
                image_np_expanded = np.expand_dims(image, axis=0)

                # Actual detection.
                (boxes, scores, classes, num) = sess.run([detection_boxes, 
                                                          detection_scores, 
                                                          detection_classes, 
                                                          num_detections],
                                                         feed_dict={image_tensor: image_np_expanded})
                
                red_flag = read_traffic_lights(image, 
                                               np.squeeze(boxes), 
                                               np.squeeze(scores), 
                                               np.squeeze(classes).astype(np.int32))

                if red_flag:
                    return TrafficLight.RED
                else:
                    return TrafficLight.GREEN

        return 0
