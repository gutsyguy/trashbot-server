import cv2
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the video capture with OpenCV
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    logging.error("Cannot open camera")
    exit()

# Set video properties
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 25)

# Define the FFmpeg command for streaming to Amazon IVS
rtmp_url = 'rtmp://<your-ivs-ingest-endpoint>:1935/<stream-key>'
ffmpeg_command = ['ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-pix_fmt', 'bgr24', 
                  '-s', '{}x{}'.format(640, 480), '-r', '25', '-i', '-', '-c:v', 'libx264', 
                  '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-f', 'flv', rtmp_url]

# Open pipe to FFmpeg
process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

# Stream video frames to FFmpeg
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error("Can't receive frame (stream end?). Exiting ...")
            break

        # Write the frame to the FFmpeg process
        process.stdin.write(frame.tobytes())

finally:
    cap.release()
    process.stdin.close()
    process.wait()
    cv2.destroyAllWindows()
    logging.info("Camera stream closed")

