# misc

## A few steps to take:
1. Download Tensorflow's object detection API
	* Clone Tensorflow's model repo
      (https://github.com/tensorflow/models)
	* Copy object_detection folder from research/object_detection to
	  ros/src/tl_detector/light_classification
	* Ultimately you should have:
	  ros/src/tl_detector/light_classification/object_detection
	  with all its contents
	  
2. Make sure you have the dependencies installed
	* Short version (only if using docker)
	  * pip install lxml matplotlib
      * apt-get install protobuf-compiler python-pil python-lxml
        python-tk
		
	* Long Version
	  + Follow https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md

3. Run the following command
	* If used docker installation:
	  cd /capstone/ros/src/tl_detector/light_classification && protoc object_detection/protos/*.proto --python_out=. && export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim && cd /capstone/ros
	* Otherwise: (substitute PATH_to_ros with a proper path to the
	  project's ros folder)
	  cd PATH_TO_ros/src/tl_detector/light_classification && protoc object_detection/protos/*.proto --python_out=. && export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim && cd PATH_TO_ros

4. Upon running roslaunch/styx.launch; wait until the message
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
