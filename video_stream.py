import cv2
import subprocess
import logging
import os
from dotenv import load_dotenv

class Video_Stream:
    def __init__(self):
        load_dotenv()
        self.stream_key = os.environ['stream_key']
        self.ffmpeg_process = None
        self.camera = None
        logging.basicConfig(level=logging.INFO)

    def start_stream(self):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            logging.error("Cannot open camera")
            exit()

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.camera.set(cv2.CAP_PROP_FPS, 25)

        rtmp_url = self.stream_key
        ffmpeg_command = [
            'ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-pix_fmt', 'bgr24',
            '-s', '{}x{}'.format(640, 480), '-r', '25', '-i', '-', '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-f', 'flv', rtmp_url
        ]

        self.ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

        try:
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    logging.error("Can't receive frame (stream end?). Exiting ...")
                    self.stop_stream()
                    break

                self.ffmpeg_process.stdin.write(frame.tobytes())

        except Exception as e:
            logging.error("An exception occurred: {}".format(e))
            self.stop_stream()

    def stop_stream(self):
        if self.camera:
            self.camera.release()
            self.camera = None
            logging.info("Camera released")

        if self.ffmpeg_process:
            self.ffmpeg_process.stdin.close()
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()
            self.ffmpeg_process = None
            logging.info("FFmpeg process terminated")
        
        cv2.destroyAllWindows()
        logging.info("All windows closed")
