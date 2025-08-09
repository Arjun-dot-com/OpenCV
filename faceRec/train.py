import os
import cv2 as cv
import numpy as np


def train():
    people=[]
    DIR='dataset'  #Assigning the directory
    haar_cascade=cv.CascadeClassifier('haar_face.xml')

    #Load person names from folders
    for folder in os.listdir(DIR):
        people.append(folder)

    features=[]
    labels=[]

    for label, person in enumerate(people):
        person_path=os.path.join(DIR, person)
        
        for image_name in os.listdir(person_path):
            img_path=os.path.join(person_path, image_name)
            img=cv.imread(img_path)
            if img is None:
                continue

            gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            faces_rect=haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

            for (x, y, w, h) in faces_rect:
                faces_roi=gray[y:y+h, x:x+w]
                features.append(faces_roi)
                labels.append(label)

    features = np.array(features, dtype='object')
    labels = np.array(labels)

    face_recognizer=cv.face.LBPHFaceRecognizer_create()

    face_recognizer.train(features, labels)

    face_recognizer.save('face_trained.yml')
    np.save('features.npy', features)
    np.save('labels.npy', labels)