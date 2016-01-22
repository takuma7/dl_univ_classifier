from flask import Flask, render_template, json, jsonify, request
from flask.ext.cors import CORS
import numpy as np
import cv2
import io

app = Flask(__name__)
CORS(app)

cascPath = './haarcascade_frontalface_alt2.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/classify", methods=['POST'])
def classify():
    if request.method == 'POST' and 'photo' in request.files:
        photo = request.files['photo']
        inmem_file = io.BytesIO()
        photo.save(inmem_file)
        data = np.fromstring(inmem_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        image = cv2.imdecode(data, color_image_flag)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    flags = cv2.CASCADE_SCALE_IMAGE
                )
        if len(faces) > 0:
            faces_list = []
            result_list = []
            for face in faces.tolist():
                x,y,w,h = face
                cx = x+w//2
                cy = y+h//2
                ll = min(w,h)
                l  = ll//2
                faces_list.append([cx-l, cy-l, ll, ll])
                face_img =image[(cy-l):(cy+l), (cx-l):(cx+l)].copy()
                img_width = 256
                r = img_width / face_img.shape[1]
                dim = (img_width, int(face_img.shape[0]*r))
                resized_face_img = cv2.resize(face_img, dim, interpolation=cv2.INTER_AREA)
                #####
                # TODO: implement here. Do something with face_img
                #####
            return  jsonify(
                        faces_num=len(faces),
                        faces=faces_list
                    )
        else:
            return jsonify(
                        faces_num=0,
                        faces=[]
                    )

if __name__ == "__main__":
    app.debug = True
    app.run()
