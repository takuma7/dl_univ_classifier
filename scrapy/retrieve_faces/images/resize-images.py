# -*- coding: utf-8 -*-
import sys
# sys.path.append('/usr/local/Cellar/opencv3/3.0.0/lib/python2.7/site-packages/')
import cv2
import os
from tqdm import tqdm
import imghdr

allowedFormats = ['jpeg', 'gif', 'png']

if len(sys.argv) < 4:
    print("Usage:\n\tpython %s <width> <src_dir_path> <dist_dir_path> " % sys.argv[0])
    exit(1)

imageWidth = int(sys.argv[1])
imageSrcDirPath = sys.argv[2]
imageDistDirPath = sys.argv[3]

if not os.path.exists(imageSrcDirPath):
    print("There is no such folder: %s" % imageSrcDirPath)
    exit(1)

if not os.path.exists(imageDistDirPath):
    os.makedirs(imageDistDirPath)
    print("mkdir: %s"  % imageDistDirPath)

listing = os.listdir(imageSrcDirPath)

def process_fpath(imagePath):
    # print(os.path.join(imageSrcDirPath, imagePath))
    if imghdr.what(os.path.join(imageSrcDirPath, imagePath)) not in allowedFormats:
        return
    image = cv2.imread(os.path.join(imageSrcDirPath, imagePath))
    r = imageWidth / image.shape[1]
    dim = (imageWidth, int(image.shape[0] * r))
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite(os.path.join(imageDistDirPath, imagePath), resized)

for imagePath in tqdm(listing):
    process_fpath(imagePath)

