# YOLO in caffe
 
__Update 12-05-2016__:  __Currently, only yolo v1 (http://pjreddie.com/darknet/yolov1/) is supported. Yolo V2 (http://pjreddie.com/darknet/yolo/) is not supported. Batch norm layer is supported.__

## Introduction

This is a caffe implementation of the YOLO:Real-Time Object Detection

Note, the caffe models are not trained in caffe, but converted from darknet's (.weight) files (http://pjreddie.com/darknet/yolov1/).

The converter is consisted of four steps:
* create .prototxt files for caffe from  .cfg file in darkent 
* initialize the caffe network and weights from .prototxt file
* read the weights from pre-trained darknet's (.weight) file
* replace the initialized weights with the weights in pre-trained darkenet's (.weight) file

## Usage 

* run "create_yolo_prototxt.py" to create .prototxt files 
* run "create_yolo_caffemodel.py" to create .caffemodel files
* run "yolo_main.py" to call yolo in caffe


## Convert yolo's (.weight) files to caffemodel

* first, you need to  download the pretrained yolo weight files (http://pjreddie.com/darknet/yolov1/) and .cfg files (https://github.com/pjreddie/darknet/tree/master/cfg/yolov1) 

* run create_yolo_prototxt.py to create .prototxt files

* after that, run create_yolo_caffemodel.py to create the caffemodel from yolo's (.weight) files 

  	* "python create_yolo_caffemodel.py -m train_val_prototxt.filename -w yoloweights_filename -o caffemodel_filename"

  replace train_val_prototxt.filename with /your/path/to/yolo_train_val.prototxt (yolo_small, yolo_tiny),
  yoloweights_filename with /your/path/to/yolo.weights (yolo-small, yolo-tiny), and caffemodel_filename with your output caffemodel name,
  
  e.g.
  "python create_yolo_caffemodel.py -m yolo_train_val.prototxt -w yolo.weights -o yolo.caffemodel" 


## Main file usage

run yolo_main.py to do yolo object detection for the input image

* "python yolo_main.py -m model_filename -w weight_filename -i image_filename"

replace model_filename with /your/path/to/yolo_small_deploy.prototxt or yolo_tiny_deploy.prototxt, 
weight_filename with /your/path/to/yolo_tiny.caffemodel or yolo_small.caffemodel and image_filename with the target image file

## Requirements

   * Caffe, pycaffe

   * Opencv2

## Copyrights
 
According to the LICENSE file of the original code,

   * Me and original author hold no liability for any damages

   * Do not use this on commercial!

## ToDoList

Generate caffe prototxt files from darknet cfg files
