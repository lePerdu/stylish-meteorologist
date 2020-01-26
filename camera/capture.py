import io

import PiCamera


def capture_image():
    camera = PiCamera()
    # Wait 2 seconds for the camera to adjsut to the conditions
    camera.sleep(2)

    camera.capture(buf)
    # TODO Is this okay? Will not closing the buffer have consequences?
    return buf.getbuffer()
