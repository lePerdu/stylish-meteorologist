import io
import time

import picamera

camera = picamera.PiCamera()


def capture_image():
    buf = io.BytesIO()
    camera.capture(buf, format='jpeg')
    # TODO Is this okay? Will not closing the buffer have consequences?
    return bytes(buf.getbuffer())
