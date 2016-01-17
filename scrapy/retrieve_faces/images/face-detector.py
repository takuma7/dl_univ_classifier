# -*- coding: utf-8 -*-
import sys
# sys.path.append('/usr/local/Cellar/opencv3/3.0.0/lib/python2.7/site-packages/')
import cv2
import os
from multiprocessing import Pool
from tqdm import tqdm

if len(sys.argv) < 5:
    print("Usage:\n\tpython %s <casc_path> <src_dir_path> <dist_dir_path> <trash_dir_path>" % sys.argv[0])
    exit(1)

cascPath = sys.argv[1]
imageSrcDirPath = sys.argv[2]
imageDistDirPath = sys.argv[3]
imageTrashDirPath = sys.argv[4]
# print(sys.argv)

if not os.path.exists(imageSrcDirPath):
    print("There is no such folder: %s" % imageSrcDirPath)
    exit(1)

if not os.path.exists(imageDistDirPath):
    os.makedirs(imageDistDirPath)
    print("mkdir: %s"  % imageDistDirPath)

if not os.path.exists(imageTrashDirPath):
    os.makedirs(imageTrashDirPath)
    print("mkdir: %s"  % imageTrashDirPath)

faceCascade = cv2.CascadeClassifier(cascPath)

listing = os.listdir(imageSrcDirPath)

def process_fpath(imagePath):
    # print(os.path.join(imageSrcDirPath, imagePath))
    image = cv2.imread(os.path.join(imageSrcDirPath, imagePath))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            # minSize=(10,10),
            flags = cv2.CASCADE_SCALE_IMAGE
            )

    # print("Found %d faces in %s" % (len(faces), imagePath))
    # if len(faces) != 1:
    if len(faces) == 0:
        # for i, (x,y,w,h) in enumerate(faces):
            # if i==0:
                # col = (0,0,255)
            # else:
                # col = (0,255,0)
            # cx = x+w//2
            # cy = y+h//2
            # ll = min(w,h)
            # l = ll//2
            # cv2.rectangle(image, (cx-l,cy-l), (cx+l, cy+l), col, 2)
        cv2.imwrite(os.path.join(imageTrashDirPath, "%d-%s" % (len(faces), imagePath) ), image)
    if len(faces) > 0:
        x,y,w,h = faces[0]
        cx = x+w//2
        cy = y+h//2
        ll = min(w,h)
        l = ll//2
        face_img =image[(cy-l):(cy+l), (cx-l):(cx+l)].copy()
        # print(os.path.join(imageDistDirPath, imagePath))
        cv2.imwrite(os.path.join(imageDistDirPath, imagePath),  face_img)

for imagePath in tqdm(listing):
    process_fpath(imagePath)

# p = Pool(4)
# p.map(process_fpath, listing)

