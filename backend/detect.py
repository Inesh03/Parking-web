import cv2
from ultralytics import YOLO
from datetime import datetime
from config import get_db

# Load YOLO model
model = YOLO("../weights/best.pt")
db = get_db()
collection = db["detections"]

video_path = "parking.mp4"
cap = cv2.VideoCapture(video_path)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # loop video
            continue

        # Run YOLO detection
        results = model(frame)
        annotated_frame = results[0].plot()

        # Count detected objects
        classes = results[0].boxes.cls.tolist()
        names = [model.names[int(c)] for c in classes]
        car_count = names.count("car")
        free_count = names.count("free")

        # Save to MongoDB
        detection_data = {
            "timestamp": datetime.now().isoformat(),
            "cars": car_count,
            "free_spaces": free_count
        }
        collection.insert_one(detection_data)

        # Encode the frame to JPEG for streaming
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
