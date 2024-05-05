# -*- coding: utf-8 -*-

import cv2
import time

# Load the cascade
#face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

def video_capture():
    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    cap.release() 
    return faces

def webcam_faces():
    # faces = video_capture()
    while 1:
        faces = video_capture()
        print(faces)
        print(type(faces))
        if isinstance(faces, tuple):
            # return False
            print("No face detected")
        else:
            # break
            print("Face detected")
    return True
        

"""   

while True:
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each faceq
    # for (x, y, w, h) in faces:
    #   cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Display
    print(faces)
    if isinstance(faces, tuple):
        print("no face")
    else:
        print("yes face")
    #cv2.imshow('img', img)
    # Stop if escape key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
cap.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
"""