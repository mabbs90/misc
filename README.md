# misc

A few steps to take:
1- Clone Tensorflow's model git (https://github.com/tensorflow/models), and put the entire 'research' directory's contents 
into ros/src/tl_detector/light_classification

2- Make sure you have the dependencies intalled (skip the protobuf compilations and library or test section)
https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md

3- Edit the last line in devel/setup.sh to make it appropriate to your own path.

4- Upon running roslaunch/styx.launch; wait until the message "SUCCESSFULLY LOADED THE GRAPH" appears in console before running the simulator.
