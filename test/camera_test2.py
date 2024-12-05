import cv2
import numpy as np
from picamera2 import Picamera2
from time import sleep

# Initialize the camera
picam2 = Picamera2()

# Configure the camera (use the default settings)
picam2.configure(picam2.create_still_configuration())

# Start the camera
picam2.start()

# Main loop to capture and display frames
try:
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Convert the captured frame to a format OpenCV can handle
        # PiCamera2 outputs a numpy array (BGR format)
        cv2.imshow("PiCamera2 Feed", frame)

        # Break the loop on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Clean up on exit
finally:
    picam2.stop()
    cv2.destroyAllWindows()