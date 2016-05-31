# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 16:10:21 2016

@author: xingw
"""

import caffe
import numpy as np
import sys, getopt

def transpose_matrix(inputWeight, rows, cols):
	inputWeight_t = np.zeros((rows*cols,1))
	for x in xrange(rows):
		for y in xrange(cols):
			inputWeight_t[y*rows + x] = inputWeight[x*cols + y]
	return inputWeight_t

def main(argv):
	model_filename = ''
	yoloweight_filename = ''
	caffemodel_filename = ''
	try:
		opts, args = getopt.getopt(argv, "hm:w:o:")
		print opts
	except getopt.GetoptError:
		print 'create_yolo_caffemodel.py -m <model_file> -w <yoloweight_filename> -o <caffemodel_output>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'create_yolo_caffemodel.py -m <model_file> -w <yoloweight_filename> -o <caffemodel_output>'
			sys.exit()
		elif opt == "-m":
			model_filename = arg
		elif opt == "-w":
			yoloweight_filename = arg
		elif opt == "-o":
			caffemodel_filename = arg
			
	print 'model file is ', model_filename
	print 'weight file is ', yoloweight_filename
	print 'output caffemodel file is ', caffemodel_filename
	net = caffe.Net(model_filename, caffe.TEST)
	params = net.params.keys()

	# read weights from file and assign to the network
	netWeightsInt = np.fromfile(yoloweight_filename, dtype=np.int32)
	transFlag = (netWeightsInt[0]>1000 or netWeightsInt[1]>1000) # transpose flag, the first 4 entries are major, minor, revision and net.seen
	print transFlag

	netWeightsFloat = np.fromfile(yoloweight_filename, dtype=np.float32)
	netWeights = netWeightsFloat[4:] # start from the 5th entry, the first 4 entries are major, minor, revision and net.seen
	print netWeights.shape
	count = 0
	for pr in params:
		biasSize = np.prod(net.params[pr][1].data.shape)
		net.params[pr][1].data[...] = np.reshape(netWeights[count:count+biasSize], net.params[pr][1].data.shape)
		count = count + biasSize
		weightSize = np.prod(net.params[pr][0].data.shape)
		if pr[0:2]=='co': # convolutional layer
			net.params[pr][0].data[...] = np.reshape(netWeights[count:count+weightSize], net.params[pr][0].data.shape)
		else: # fc layer
			dims = net.params[pr][0].data.shape
			if transFlag: # need transpose for fc layers
				net.params[pr][0].data[...] = np.reshape(transpose_matrix(netWeights[count:count+weightSize], dims[1],dims[0]), dims)
			else:
				net.params[pr][0].data[...] = np.reshape(netWeights[count:count+weightSize], dims)
		count = count + weightSize
	print count
	net.save(caffemodel_filename)		
		
if __name__=='__main__':	
	main(sys.argv[1:])
