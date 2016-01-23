import os
import sys
#import dlib
from skimage import io
import numpy as np
#import cv2
import argparse
import os
from PIL import Image
import six
import cPickle as pickle
from six.moves import queue
import random
import nin


parser = argparse.ArgumentParser(
    description='Learning convnet from ILSVRC2012 dataset')
parser.add_argument('--image', help='Path to image')
parser.add_argument('--mean', '-m', default='mean.npy',
                    help='Path to the mean file (computed by compute_mean.py)')

parser.add_argument('--model', '-mo', default='model',
                    help='Path to the model file')
args = parser.parse_args()

mean_image = pickle.load(open(args.mean, 'rb'))
model = pickle.load(open(args.model,'rb'))

cropwidth = 256 - model.insize 




def read_image(src_img, center=True, flip=False):
    # Data loading routine
    image = np.asarray(Image.open(src_img)).transpose(2, 0, 1)
    #image = src_img.transpose(2, 0, 1)
    if center:
        top = left = cropwidth / 2
    else:
        top = random.randint(0, cropwidth - 1)
        left = random.randint(0, cropwidth - 1)
    bottom = model.insize + top
    right = model.insize + left

    image = image[:, top:bottom, left:right].astype(np.float32)
    image -= mean_image[:, top:bottom, left:right]
    image /= 255
    return image


f = open('labeled_data_m_256_test.txt')
lines = f.readlines()
num_lines = 0
count = 0

for line in lines:
	num_lines +=1
	img_path = line.split()[0]
	label_univ = line.split()[1]
	x = np.ndarray((1, 3, model.insize, model.insize), dtype=np.float32)
	x[0]= read_image(args.image)
	score = model.predict(x)
	print score
	index_univ = np.argsort(score[0])
	pred_univ = index_univ[0]
	if pred_univ == label_univ:
		count += 1
correct_ratio = count / num_lines

return correct_ratio





