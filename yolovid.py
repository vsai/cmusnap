import picamera
import time

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.start_recording('swaggerswag.h264')
time.sleep(5)
camera.stop_recording()


#with picamera.PiCamera() as camera:
#	camera.resolution = (640, 480)
#	camera.start_recording('my_vid.h264', inline_headers=False)
#	camera.wait_recording(4)
#	camera.stop_recording()
