import cv2
import os


def capture(name):
    output_dir = f"dataset/{name}"
    num_images_to_capture = 50

    if not os.path.exists(output_dir):
        os.makedirs(output_dir) #create a folder

    haar_cascade=cv2.CascadeClassifier('haar_face.xml')
    cap=cv2.VideoCapture(0)

    count=0

    while True:
        success, frame=cap.read()
        if not success:
            print("Failed to capture frame.")
            break

        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=15)

        for (x, y, w, h) in faces:
            face=gray[y:y+h, x:x+w]
            face=cv2.resize(face, (200, 200))  #Resizing the image for consistency

            count+=1
            cv2.imwrite(f"{output_dir}/{name}_{count}.jpg", face)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{count}/{num_images_to_capture}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Capturing Faces", frame)

        if cv2.waitKey(1) & 0xFF==ord('q') or count>=num_images_to_capture:
            break

    cap.release()
    cv2.destroyAllWindows()
