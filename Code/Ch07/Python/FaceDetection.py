import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2

switchPin =26

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(switchPin, GPIO.OUT)
GPIO.setwarnings(False)

# Load pre-trained MobileNet SSD model for face detection
net = cv2.dnn.readNetFromCaffe('/home/pi/RPi/Code/Python/model/deploy.prototxt', '/home/pi/RPi/Code/Python/model/mobilenet_iter_73000.caffemodel')

# Video capture setup
picam2 = Picamera2()
picam2.preview_configuration.main.size = (980,460)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

while True:
    # Read a frame from the camera
    img = picam2.capture_array()

    # Prepare the frame for face detection
    blob = cv2.dnn.blobFromImage(img, 0.007843, (300, 300), 127.5)
    net.setInput(blob)

    # Perform face detection
    detections = net.forward()

    # Check for face presence in the detected regions
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Adjust the confidence threshold as needed
            GPIO.output(switchPin, GPIO.HIGH)
            print("Face detected - Relay ON")
            time.sleep(1)
            break
        else:
            GPIO.output(switchPin, GPIO.LOW)
            print("No face detected - Relay OFF")

    # Display the frame
    cv2.imshow("Face Detection", img)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Cleanup GPIO and release resources
GPIO.cleanup()
cv2.destroyAllWindows()
