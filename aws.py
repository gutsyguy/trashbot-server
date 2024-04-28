import cv2
import boto3
import logging

logging.basicConfig(level=logging.INFO)

cap = cv2.VideoCapture(0)  
if not cap.isOpened():
    logging.error("Cannot open camera")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 20)

kinesis_client = boto3.client('kinesisvideo')

endpoint = kinesis_client.get_data_endpoint(
    StreamName='YourKinesisVideoStream',
    APIName='PUT_MEDIA'
)['DataEndpoint']

kvs_client = boto3.client('kinesis-video-media', endpoint_url=endpoint)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error("Can't receive frame (stream end?). Exiting ...")
            break

        _, buffer = cv2.imencode('.jpg', frame)

        kvs_client.put_media(
            StreamName='YourKinesisVideoStream',
            Payload=buffer.tobytes(),
            FragmentTimecodeType='RELATIVE'
        )

finally:
    cap.release()
    cv2.destroyAllWindows()
    logging.info("Camera stream closed")

