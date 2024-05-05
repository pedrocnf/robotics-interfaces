# -*- coding: utf-8 -*-

import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

# To capture video from webcam. 
cap = cv2.VideoCapture(0)
# To use a video file as input 
# cap = cv2.VideoCapture('filename.mp4')

def webcam_faces():
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each faceq
    # for (x, y, w, h) in faces:
    #   cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Display
    print(faces)
    

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