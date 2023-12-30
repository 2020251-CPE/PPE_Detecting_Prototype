from flask import Flask, render_template, Response, jsonify, request
from datetime import datetime
from ultralytics import YOLO    
from flask_cors import CORS
import queries as que
import googleMod as go
import threading
import socket
import time
import cv2
import os

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
os.makedirs('screenshots', exist_ok=True)
# Load YOLO model
model = YOLO('finalBest.pt')
# Open camera
cap = cv2.VideoCapture(0)

now = datetime.now()
show_live_camera = True  # Flag to toggle between live camera and uploaded content
last_screenshot_time = time.time()  # Variable to track the last screenshot time
screenshot_interval = 6  # Set the interval for taking screenshots (in seconds)

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
                   b'Content-Type: image/jPower Management Unit peg\r\n\r\n' + frame + b'\r\n')
            
def take_screenshot(results):
    '''Takes a Screenshot and saves it to a designated directory'''
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_fileLoc = f'screenshots/screenshot{current_time}.jpg' #temporary local storage
    googleFileName = screenshot_fileLoc[len('screenshots/'):-len('.jpg')]
    cv2.imwrite(screenshot_fileLoc, results[0].plot())

    # Uploads screenshot to Google Drive
    classArray = results[0].boxes.cls.numpy().copy()
    objArray = [0] * (max(results[0].names)+1)
    for value in classArray:
        objArray[int(value)] += 1 # Counts the frequencies a class(index) is detected in frame 
    newPic = go.upload_to_folder(go.search_drive(datetime.now().strftime("%Y-%m-%d"))[0]['id'],googleFileName)

    # Uploads screenshot metadata to postgres Database
    que.upload_metadata(
        filename=googleFileName,                                        # file Name
        fileLoc=f'https://drive.google.com/file/d/{newPic}/view',       # file URL (Google Drive)
        hostName=socket.gethostname(),                                  # Hostname
        datetime=datetime.strftime(current_time,"%Y-%m-%d %H:%M:%S"),   # Date Time
        array=objArray                                                  # Object Count Array
        )
    
    # Delete Photos from temp directory 
    try:
        os.remove(screenshot_fileLoc) #Delete Screenshot in local machine Permanently
        folder_name = "screenshots"
        folder_path = os.path.join(os.path.dirname(__file__), folder_name)
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")
    except FileNotFoundError:
        print(f"File '{screenshot_fileLoc}' not found. Skipping removal.")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/')
def index():
    cloudFileName = datetime.now().strftime("%Y-%m-%d") 
    if go.search_drive(cloudFileName) == []:
        go.create_folder(cloudFileName)
        print(f'Folder {cloudFileName} created')
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    if show_live_camera:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/allLogs/<option>',methods=['GET'])    
def all_logs(option:str):
    if request.method == 'GET' and (option.lower() == 'all' or option.lower()== 'today'):
        # Sample URL Argument: ?aC=1 is equal to apronCount is not equal to 0
        args_list = ['aC', 'bSC', 'mC', 'gLC', 'gOC', 'hCC']
        boolArr = [True if request.args.get(arg) is None else False for arg in args_list]
        print(boolArr)
        return jsonify(que.get_logs(option,boolArr))
    else:
        return 'Invalid request method or Invalid Route'

@app.route('/allCols',methods=['GET'])
def log_cols():
    if request.method == 'GET':
        return jsonify(que.get_log_cols())
    else:
        return 'Invalid request method or Invalid Route'
    

@app.route('/ping', methods=['GET']) #for San Checks
def ping_pong():
    return jsonify('pong!')
    
# Run this when in dev    
if __name__ == '__main__':
    try:
        app.run(debug=True, threaded=True)
    except KeyboardInterrupt:
        folder_name = "screenshots"
        folder_path = os.path.join(os.path.dirname(__file__), folder_name)
        file_list = os.listdir(folder_path)
        print("Removing screenshots")  
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
        print("Exiting gracefully.")        