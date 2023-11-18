from flask import Flask, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ultralytics import YOLO
import threading
import numpy
import time
import cv2
import os

app = Flask(__name__)


os.makedirs('screenshots', exist_ok=True)
# Load YOLO model
model = YOLO('finalBest.pt')
# Open camera
cap = cv2.VideoCapture(0)

now = datetime.now()
show_live_camera = True  # Flag to toggle between live camera and uploaded content
last_screenshot_time = time.time()  # Variable to track the last screenshot time
screenshot_interval = 2  # Set the interval for taking screenshots (in seconds)

def generate_frames():
    global last_screenshot_time
    while show_live_camera:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            results = model.track(frame, persist=True)

            if results and results[0].boxes:
                current_time = time.time()
                if current_time - last_screenshot_time >= screenshot_interval:
                    screenshot_thread = threading.Thread(target=take_screenshot, args=(results,))
                    screenshot_thread.start()  # Start a thread to take a screenshot
                    last_screenshot_time = current_time

            frame = results[0].plot()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
def take_screenshot(results):
    '''Takes a Screenshot and saves it to a designated directory'''
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_filename = f'screenshots/screenshot{current_time}.jpg'
    cv2.imwrite(screenshot_filename, results[0].plot())
    print(f'Screenshot saved: {screenshot_filename}')  # FileLocation
    classArray = results[0].boxes.cls.numpy().copy()
    objArray = [0] * (max(results[0].names)+1)
    for value in classArray:
        objArray[int(value)] += 1 # Counts the frequencies a class(index) is detected in frame
    print(objArray) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    if show_live_camera:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
if __name__ == '__main__':
    app.run(debug=True)
