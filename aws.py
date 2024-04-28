import cv2
import subprocess
import logging
import os
from dotenv import load_dotenv

load_dotenv()
stream_key = os.environ["stream_key"]
logging.basicConfig(level=logging.INFO)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    logging.error("Cannot open camera")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 25)

rtmp_url = stream_key
ffmpeg_command = ['ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-pix_fmt', 'bgr24', 
                  '-s', '{}x{}'.format(640, 480), '-r', '25', '-i', '-', '-c:v', 'libx264', 
                  '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-f', 'flv', rtmp_url]

print("____________________________-")
print(ffmpeg_command)
print("____________________________-")

process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error("Can't receive frame (stream end?). Exiting ...")
            break

        process.stdin.write(frame.tobytes())

finally:
    cap.release()
    process.stdin.close()
    process.wait()
    cv2.destroyAllWindows()
    logging.info("Camera stream closed")

