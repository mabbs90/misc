# misc

## A few steps to take:
0. Copy only two files from this repo to yours
   * Replace your tl_detector.py with this repo's tl_detector.py
   * Replace your tl_classifier.py with this repo's tl_classifier.py

`. Upon running roslaunch launch/styx.launch; wait until the message
"SUCCESSFULLY LOADED THE GRAPH" appears in console before running the
simulator.
	* During the first attempt, the program tries to download the
      tensorflow pretrained model from object detection API. You will
      get a message in console that the download is beginning and when
      the download is finished. If by any chance it did not succeed,
      download the model manually from the following link, unzip it
      and put its folder under
      PATH_TO_ros/src/tl_detector/light_classification
	  link to download the model:
	  'http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet101_coco_11_06_2017'
