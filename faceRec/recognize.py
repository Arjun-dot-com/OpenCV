import cv2 as cv
import numpy as np
import os

def recognize():
    #load the trained face recognizer model
    face_recognizer=cv.face.LBPHFaceRecognizer_create()
    face_recognizer.read('face_trained.yml')

    haar_cascade=cv.CascadeClassifier('haar_face.xml')
    DIR='dataset'
    people=[folder for folder in os.listdir(DIR)]

    cap=cv.VideoCapture(0) #0 as it is laptop screen, you can keep 1, 2, 3 and so on for external cameras 

    while True:
        isTrue, frame=cap.read()
        if not isTrue:
            print("Failed to read frame from webcam.")
            break

        gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces_rect=haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

        for (x, y, w, h) in faces_rect:
            faces_roi=gray[y:y+h, x:x+w]

            label, confidence=face_recognizer.predict(faces_roi)

            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv.putText(frame, str(people[label]), (x, y-10), 
                       cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            cv.putText(frame, f"{int(confidence)}", (x, y+h+30),
                       cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv.imshow('Face Recognition', frame)

        if cv.waitKey(1) & 0xFF==ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()