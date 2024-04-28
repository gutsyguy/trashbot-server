from flask import Flask, jsonify, request
import subprocess
from video_stream import Video_Stream
from time import sleep
from robot.py import Init, ForwardStride, TrayCollection

app = Flask(__name__)
video_stream = Video_Stream()
Init()


broadcast_process = None
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': "Easy"})

@app.route('/api/start', methods=['POST'])
def start_broadcast():
    global broadcast_process
    if broadcast_process is not None:
        return jsonify({'message': 'Broadcast already running'}), 400
    
    video_stream.start_stream()

    broadcast_process = subprocess.Popen(command)
    return jsonify({'message': 'Broadcast started'}), 200

@app.route('/api/stop', methods=['POST'])
def stop_broadcast():
    global broadcast_process
    # if broadcast_process is None:
        # return jsonify({'message': 'Broadcast not running'}), 400
    
    video_stream.stop_stream()
    # broadcast_process.terminate()
    broadcast_process = None
    return jsonify({'message': 'Broadcast stopped'}), 200

@app.route('/api/moveForward', methods = ["GET"])
def forward():
    return "Moved forward"

@app.route('/api/moveBackward', methods = ["GET"])
def backward():
    return "Moved backward"

@app.route('/api/turnRight', methods = ["GET"])
def right():
    return "Turned Right"


@app.route('/api/turnLeft', methods = ["GET"])
def left():
    return "Turned Left"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
