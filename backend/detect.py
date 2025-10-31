import cv2
import numpy as np
from ultralytics import YOLO
from shapely.geometry import Polygon, box
from shapely.errors import TopologicalError
import json
from pymongo import MongoClient
from datetime import datetime

# === Load YOLOv11 model ===
model = YOLO("../weights/best.pt")

# === Load parking spot polygons ===
with open("parking_spots.json") as f:
    raw_spots = json.load(f)

# Clean polygons (fix invalid or self-intersecting ones)
parking_spots = {}
for spot_id, coords in raw_spots.items():
    poly = Polygon(coords)
    if not poly.is_valid:
        poly = poly.buffer(0)  # automatically fix invalid geometry
    parking_spots[spot_id] = poly

# === Connect to MongoDB ===
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["parking_db"]
    return db

# === Initialize video ===
cap = cv2.VideoCapture("parking.mp4")

# --- Helper: Safe IoU computation
def safe_iou(poly1, poly2):
    """Compute IoU safely; return 0 if invalid geometry causes error."""
    try:
        inter_area = poly1.intersection(poly2).area
        union_area = poly1.union(poly2).area
        return inter_area / union_area if union_area > 0 else 0
    except TopologicalError:
        return 0

# --- Core detection function
def get_slot_status(frame):
    db = get_db()

    # Resize to match video resolution
    frame = cv2.resize(frame, (1920, 1080))

    # YOLO inference (stride-aligned)
    results = model(frame, imgsz=(1920, 1088), verbose=False)[0]

    car_boxes = []
    for box_info in results.boxes:
        x1, y1, x2, y2 = box_info.xyxy[0]
        label = int(box_info.cls[0])
        if label == 0:  # car class
            car_boxes.append([float(x1), float(y1), float(x2), float(y2)])

    slot_status = {}

    for spot_id, spot_poly in parking_spots.items():
        occupied = False
        for (x1, y1, x2, y2) in car_boxes:
            car_poly = box(x1, y1, x2, y2)
            if safe_iou(spot_poly, car_poly) > 0.2:
                occupied = True
                break
        slot_status[spot_id] = "occupied" if occupied else "free"

    # Store latest result
    db["slot_status"].insert_one({
        "timestamp": datetime.now(),
        "status": slot_status
    })

    return slot_status


# --- Debug visualizer ---
if __name__ == "__main__":
    cv2.namedWindow("Parking Status Debug", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Parking Status Debug", 960, 540)

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = cv2.resize(frame, (1920, 1080))
        status = get_slot_status(frame)

        for spot_id, spot_poly in parking_spots.items():
            pts = np.array(list(spot_poly.exterior.coords), np.int32)
            color = (0, 255, 0) if status[spot_id] == "free" else (0, 0, 255)
            cv2.polylines(frame, [pts], True, color, 2)
            center = np.mean(pts, axis=0).astype(int)
            cv2.putText(frame, spot_id.replace("spot_", ""), tuple(center),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        # Overlay free/occupied counts
        free = sum(1 for v in status.values() if v == "free")
        occupied = sum(1 for v in status.values() if v == "occupied")
        cv2.putText(frame, f"Free: {free} | Occupied: {occupied}",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("Parking Status Debug", frame)
        key = cv2.waitKey(20) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
