from flask import Flask, jsonify, request
import subprocess
from video_stream import Video_Stream

app = Flask(__name__)
video_stream = Video_Stream()

broadcast_process = None
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': "Easy"})

@app.route('/start', methods=['POST'])
def start_broadcast():
    global broadcast_process
    if broadcast_process is not None:
        return jsonify({'message': 'Broadcast already running'}), 400
    
    # Command to start broadcasting (replace with your actual command)
    video_stream.start_stream()

    # Start the broadcast process
    broadcast_process = subprocess.Popen(command)
    return jsonify({'message': 'Broadcast started'}), 200

@app.route('/stop', methods=['POST'])
def stop_broadcast():
    global broadcast_process
    if broadcast_process is None:
        return jsonify({'message': 'Broadcast not running'}), 400
    
    # Stop the broadcast process
    video_stream.stop_stream()
    broadcast_process.terminate()
    broadcast_process = None
    return jsonify({'message': 'Broadcast stopped'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
