import io
import time

import picamera
import cv2 as cv
import numpy as np


def capture_image():
    with picamera.PiCamera() as camera:
        camera.rotation = 180
        time.sleep(1)
        buf = io.BytesIO()
        camera.capture(buf, format='jpeg')

        frame = cv.imdecode(np.array(buf.getbuffer()), cv.IMREAD_COLOR)

        buf.close()

        height, width, _ = frame.shape
        begin_crop = int(width / 3)
        end_crop = int(width - width / 3)
        frame = frame[:, begin_crop:end_crop]

        #cv.imshow('Capture', frame)
        #cv.waitKey(1000)
        #cv.destroyAllWindows()

        success, frame_bytes = cv.imencode('.jpg', frame)
        if not success:
            raise Exception("Could not encode image")

        # TODO Is this okay? Will not closing the buffer have consequences?
        return bytes(frame_bytes)
