import numpy as np
"""
import imutils
import time
"""
import cv2
"""
import os
import math
"""
# system libraries
import os
"""
import sys
from threading import Timer
import shutil
import time
"""

def create_dataset_folders(dataset_path, labels):
    for label in labels:
        dataset_folder = dataset_path + "\\" + label
        if not os.path.exists(dataset_folder):
            os.makedirs(dataset_folder)





# define paths and labels

dataset_path = 'C:/Users/Korisnik/Desktop/faks/dataSet'
face_model_path = 'C:/Users/Korisnik/Desktop/faks/face_detector'
labels = ["neutral", "happy", "sad", "angry"]

# caffe model for face detection, loading existing files
print("[INFO] loading face detector model...")
weightsPath = "C:/Users/Korisnik/Desktop/faks/face_detector/res10_300x300_ssd_iter_140000.caffemodel"
prototxtPath = "C:/Users/Korisnik/Desktop/faks/face_detector/deploy.prototxt"


THRESHOLD = 0.5

def capture_face_expression(face_expression, key):
    if len(face_expression) != 0:
        if key == 1:
            label = "happy"
        elif key == 2:
            label = "neutral"

        elif key == 3:
             label = "angry"

        elif key == 4:
            label = "sad"

        dataset_folder = dataset_path + "\\" + label
        number_files = len(os.listdir(dataset_folder))  # dir is directory path
        image_path = "%s\\%s_%d.jpg" % (dataset_folder, label, number_files)
        cv2.imwrite(image_path, face_expression)
    else:
        print("[ERROR] Don't exist face expression picture!")


def detect_face(frame, faceNet):
    # grab the dimensions of the frame and then construct a blob from it
    global detections
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    locs = []
    maxConf = -1
    maxIndex = -1


    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is greater than the minimum confidence
        if(confidence > THRESHOLD and confidence > maxConf):
            maxConf = confidence
            maxIndex = i

    # compute the (x, y)-coordinates of the bounding box for the object
    box = detections[0, 0, maxIndex, 3:7] * np.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")

    # ensure the bounding boxes fall within the dimensions of the frame
    (startX, startY) = (max(0, startX), max(0, startY))
    (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

    # add the face and bounding boxes to their respective lists
    locs.append((startX, startY, endX, endY))

    return (locs)




# Read deep learning network represented in one of the supported formats
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

print("[INFO] Creating dataset folders...")
create_dataset_folders(dataset_path, labels)

cap = cv2.VideoCapture(0)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    (h, w) = frame.shape[:2]
    # Convert into gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    locs = detect_face(frame, faceNet)
    face_expression = None
    for box in locs:
        # unpack the bounding box and predictions
        (startX, startY, endX, endY) = box
        face_expression = gray[startY:endY, startX:endX].copy()
        cv2.rectangle(gray, (startX, startY), (endX, endY), (255, 255, 255), 2)

    # show video stream
    cv2.putText(gray, "N - Neutral", (w - 110, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(gray, "H - Happy", (w - 110, 35), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(gray, "S - Sad", (w - 110, 55), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(gray, "A - Angry", (w - 110, 75), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(gray, "Q - Quit", (w - 110,  95), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
    cv2.imshow('frame', gray)

    # wait for key press
    key = cv2.waitKey(1)
    if key == ord('q') or key == ord('Q'):
        break
    elif key == ord('h') or key == ord('H') :
        capture_face_expression(face_expression, 1)
        print("[INFO] Happy")
    elif key == ord('n') or key == ord('N'):
        capture_face_expression(face_expression, 2)
        print("[INFO] Neutral")

    elif key == ord('a') or key == ord('A'):
        capture_face_expression(face_expression, 3)
        print("[INFO] Angry")
    elif key == ord('s') or key == ord('S'):
        capture_face_expression(face_expression, 4)
        print("[INFO] Sad")

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()