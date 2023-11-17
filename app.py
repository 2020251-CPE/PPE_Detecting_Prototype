from flask import Flask, render_template, Response
from ultralytics import YOLO
from datetime import datetime
from collections import Counter 
import numpy as np
import cv2
import time
import os

app = Flask(__name__)
now = datetime.now()
os.makedirs('screenshots', exist_ok=True)
# Load YOLO model
model = YOLO('finalBest.pt')


# Open camera
cap = cv2.VideoCapture(0)
show_live_camera = True  # Flag to toggle between live camera and uploaded content

def generate_frames():
    while show_live_camera:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            results = model.track(frame, persist=True)

            if results and results[0].boxes:
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Save a screenshot
                screenshot_filename = f'screenshots/screenshot{current_time}.jpg'
                cv2.imwrite(screenshot_filename, results[0].plot())
                print(f'Screenshot saved: {screenshot_filename}')
                print(f'screenshot{current_time}.jpg')

                # create frequency array of objects detected
                classArray = results[0].boxes.cls.numpy().copy()
                objArray = [0] * (max(results[0].names)+1)
                for value in classArray:
                    objArray[int(value)] += 1
                pDerint(objArray) 
                time.sleep(2)

            frame = results[0].plot()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    if show_live_camera:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
if __name__ == '__main__':
    app.run(debug=True)