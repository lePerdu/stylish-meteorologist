import io
import time

import picamera


def capture_image():
    camera = picamera.PiCamera()
    # Wait 2 seconds for the camera to adjsut to the conditions
    time.sleep(2)

    camera.capture(buf)
    # TODO Is this okay? Will not closing the buffer have consequences?
    return buf.getbuffer()
