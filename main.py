import cv2
from ultralytics import YOLO
import os


FRAME_WIDTH = 640
FRAME_HEIGHT = 480
OUTPUT_FILENAME = "detection_output.mp4"

# Loading a Pre-trained YOLOv8 Model  - right now, 'yolov8n.pt' is the fast "nano" model
#  this is the model used for object detection

try:
    model = YOLO('yolov8n.pt')

except Exception as e:
    print(f"Error loading YOLO model: {e}")
    print("Please ensure you have an internet connection for the initial download.")
    exit()

class_names = model.names

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(OUTPUT_FILENAME, fourcc, 20.0, (FRAME_WIDTH, FRAME_HEIGHT))

if not out.isOpened():
    print(f"Error: Could not open video writer for file {OUTPUT_FILENAME}.")
    cap.release()
    exit()

print("Starting webcam feed...")
print("Press 'q' in the video window to quit and save.")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to capture frame.")
        break
    
    frame_flipped = cv2.flip(frame, 1)
    
    results = model(frame_flipped, stream=True, verbose=False)
    
    for r in results:
        boxes = r.boxes
        
        for box in boxes:
            confidence = box.conf[0]
            
            if confidence > 0.5:
                x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0]]

                cls_id = int(box.cls[0])
                class_name = class_names[cls_id]

                cv2.rectangle(frame_flipped, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{class_name}: {confidence:.2f}"
                (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)

                cv2.rectangle(frame_flipped, (x1, y1 - text_height - 10), (x1 + text_width, y1), (0, 255, 0), -1)
                cv2.putText(frame_flipped, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    out.write(frame_flipped)

    cv2.imshow("Real-time Object Detection (Press 'q' to quit)", frame_flipped)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("'q' pressed. Shutting down...")
        break

cap.release()
out.release()
cv2.destroyAllWindows()