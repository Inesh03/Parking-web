# 🚗 Real-Time Parking Space Detection Web Application

A **full-stack computer vision project** that detects and monitors the availability of parking spaces in real time using a **YOLOv11 Nano model**, **Flask backend**, **MongoDB database**, and a **dynamic web dashboard** with live SVG-based visualization.

This system is designed to automatically identify *free* and *occupied* parking slots from a live video feed or prerecorded CCTV footage of a parking lot.

---

## 🧠 Overview

The goal of this project is to build a lightweight, real-time web application capable of:
- Detecting cars and free parking spaces from a video input using a trained YOLOv11 model.
- Storing slot occupancy data in MongoDB for historical and live analysis.
- Displaying an interactive **web dashboard** showing the current status of all parking slots (green = free, red = occupied).

---

## 🏗️ Project Architecture

```
parking-app/
├── backend/
│   ├── app.py                  # Flask web server
│   ├── detect.py               # YOLO detection + MongoDB storage
│   ├── parking_spots.json      # Polygon coordinates for parking slots
│   ├── weights/
│   │   └── best.pt             # Trained YOLOv11 nano weights
│   ├── parking.mp4             # Sample parking lot video
│   └── templates/
│       └── index.html          # Frontend dashboard (SVG visualization)
├── .venv/                      # Virtual environment (optional)
├── requirements.txt            # All dependencies
└── README.md                   # This file
```

---

## ⚙️ Core Technologies

| Component | Technology |
|------------|-------------|
| **Object Detection** | YOLOv11 Nano (Ultralytics) |
| **Backend Framework** | Flask (Python) |
| **Database** | MongoDB |
| **Frontend Visualization** | HTML, CSS, JavaScript, SVG |
| **Video Processing** | OpenCV |
| **Geometry** | Shapely |
| **Threading** | Python `threading` |

---

## 📊 Model Metrics

| Metric | Score |
|---------|--------|
| **mAP@50** | 0.9047 |
| **mAP@50-95** | 0.6132 |
| **Precision** | 0.9324 |
| **Recall** | 0.8618 |
| **Classes** | `car (id:0)` → 0.5694 mAP@50-95, `free (id:1)` → 0.6570 mAP@50-95 |

---

## 🔧 Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/parking-app.git
cd parking-app
```

### 2️⃣ Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.\.venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Start MongoDB locally
```bash
brew services start mongodb-community  # macOS
sudo service mongod start              # Linux
```

### 5️⃣ Run the app
```bash
cd backend
python app.py
```
Visit **http://127.0.0.1:5000** to open the dashboard.

---

## 🧠 Backend Endpoints

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/` | GET | Renders the web dashboard |
| `/slots` | GET | Returns latest slot occupancy from MongoDB |
| `/spots_data` | GET | Returns parking lot polygon coordinates |

---

## 🧑‍💻 Contributors

| Name | Role | Contribution |
|------|------|---------------|
| **Inesh S T** | Developer & Researcher | Model training, Flask & visualization debugging, deployment |
| **[Anirudh R](https://github.com/anirudhr04)** | Collaborator | Frontend integration, full-stack development|


---

## 🌟 Acknowledgments

- **Ultralytics YOLOv11**
- **MongoDB**
- **OpenCV & Shapely**

---
