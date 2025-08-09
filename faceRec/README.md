# Facial Recognition Software

A real-time facial recognition system built with Python and OpenCV. It captures faces via webcam, trains a recognizer using the LBPH algorithm, and identifies known individuals with live logging.

---

## 📦 Features

- Capture face images from webcam
- Train a recognizer on labeled faces
- Real-time face recognition using webcam
- Logs recognized faces with timestamp and confidence
- Simple, modular scripts for each step

---

## 🗂️ Project Structure

facial_recognition_project/
├── dataset/ # Face images stored by name
├── scripts/
│ ├── capture_faces.py # Script to collect face data
│ ├── train.py # Script to train recognizer
│ ├── recognize_with_log.py # Real-time recognition + CSV logging
├── haar_face.xml # Haar Cascade for face detection 
├── face_trained.yml # Trained recognizer model 
├── recognition_log.csv # Log of recognitions 
├── README.md # This file