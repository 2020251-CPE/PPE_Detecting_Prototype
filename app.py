from flask import Flask, render_template, Response
from dotenv import load_dotenv
from datetime import datetime
from ultralytics import YOLO
import threading
import psycopg2
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

load_dotenv()
conn = psycopg2.connect(
        host= os.getenv('DB_HOST'),
        database= os.getenv('DB_NAME'),
        user= os.getenv('DB_USER'),
        password= os.getenv('DB_PASSWORD'),
        sslmode='require'
        )

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
    screenshot_fileLoc = f'screenshots/screenshot{current_time}.jpg'
    screenshot_filename = f'screenshot{current_time}.jpg'
    cv2.imwrite(screenshot_fileLoc, results[0].plot())
    print(f'Screenshot saved: {screenshot_fileLoc}')  # FileLocation
    classArray = results[0].boxes.cls.numpy().copy()
    objArray = [0] * (max(results[0].names)+1)
    for value in classArray:
        objArray[int(value)] += 1 # Counts the frequencies a class(index) is detected in frame 

    upload_metadata(screenshot_filename,screenshot_fileLoc,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),objArray)

def upload_metadata(filename,fileLoc,datetime,array):
    '''Uploads Screenshot Metadata to Database'''
    cur = conn.cursor()
    cur.execute(
        query='INSERT INTO ppe_log (photoName,photoURL,dateAndTime,apronCount,bunnysuitCount,maskCount,glovesCount,gogglesCount,headcapCount) VALUES (%s, %s, %s,%s, %s, %s, %s, %s,%s)',
        vars=(filename, fileLoc, datetime, array[0], array[1], array[2], array[3], array[4], array[5])
        )
    conn.commit()
    cur.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    if show_live_camera:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
if __name__ == '__main__':
    app.run(debug=True)
