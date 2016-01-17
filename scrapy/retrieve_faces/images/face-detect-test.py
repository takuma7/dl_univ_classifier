import sys
# sys.path.append('/usr/local/Cellar/opencv3/3.0.0/lib/python2.7/site-packages/')
import cv2

cascPath = sys.argv[1]
imagePath = sys.argv[2]
# print(sys.argv)

faceCascade = cv2.CascadeClassifier(cascPath)

image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        # minSize=(10,10),
        flags = cv2.CASCADE_SCALE_IMAGE
        )

print("Found %d faces in %s" % (len(faces), imagePath))
i = 0
for (x,y,w,h) in faces:
    if i==0:
        col = (0,0,255)
    else:
        col = (0,255,0)
    cx = x+w//2
    cy = y+h//2
    ll = min(w,h)
    l = ll//2
    face_imgs.append(image[(cy-l):(cy+l), (cx-l):(cx+l)].copy())
    cv2.rectangle(image, (cx-l,cy-l), (cx+l, cy+l), col, 2)
    i += 1

cv2.namedWindow("Faces found", cv2.WINDOW_OPENGL | cv2.WINDOW_AUTOSIZE)
cv2.imshow("Faces found", image)
for i, face_img in enumerate(face_imgs):
    cv2.namedWindow("Face %d" % i, cv2.WINDOW_OPENGL) # | cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Face %d" % i, face_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

