import io
import time

import picamera


def capture_image():
    with picamera.PiCamera() as camera:
        buf = io.BytesIO()
        camera.capture(buf, format='jpeg')
        # TODO Is this okay? Will not closing the buffer have consequences?
        return bytes(buf.getbuffer())
