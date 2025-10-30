from flask import Flask, render_template, Response, jsonify
from detect import generate_frames, get_db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/latest_data')
def latest_data():
    db = get_db()
    latest = db["detections"].find().sort("_id", -1).limit(1)
    data = list(latest)
    if data:
        return jsonify({
            "cars": data[0]["cars"],
            "free_spaces": data[0]["free_spaces"]
        })
    return jsonify({"cars": 0, "free_spaces": 0})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
