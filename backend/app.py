from flask import Flask, render_template, Response, jsonify
from threading import Thread
from detect import get_slot_status, cap, get_db
import time
import cv2

app = Flask(__name__)

def background_detection():
    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        frame = cv2.resize(frame, (1920, 1080))  # ✅ Match detect.py
        get_slot_status(frame)
        time.sleep(1)  # run YOLO every 1 second

Thread(target=background_detection, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/slots')
def get_slots():
    db = get_db()
    latest = db["slot_status"].find().sort("_id", -1).limit(1)
    data = list(latest)
    if data:
        return jsonify(data[0]["status"])
    return jsonify({})
import json
import os
from flask import jsonify

@app.route('/spots_data')
def get_spots_data():
    spots_path = os.path.join(os.path.dirname(__file__), "parking_spots.json")
    if not os.path.exists(spots_path):
        return jsonify({"error": "parking_spots.json not found"}), 404
    with open(spots_path, "r") as f:
        spots_data = json.load(f)
    return jsonify(spots_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
