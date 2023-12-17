import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setwarnings(False)

# Load pre-trained MobileNet SSD model for face detection
net = cv2.dnn.readNetFromCaffe('C:/Users/...in same folder.../deploy.prototxt', 'C:/Users/...in same folder.../mobilenet_iter_73000.caffemodel')

# Video capture setup
video = cv2.VideoCapture(0)
video.set(3, 640)  # Set the width
video.set(4, 480)  # Set the height

while True:
    # Read a frame from the camera
    ret, frame = video.read()

    # Prepare the frame for face detection
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)

    # Perform face detection
    detections = net.forward()

    # Check for face presence in the detected regions
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Adjust the confidence threshold as needed
            GPIO.output(12, GPIO.HIGH)
            print("Face detected - Relay ON")
            time.sleep(1)
            break
        else:
            GPIO.output(12, GPIO.LOW)
            print("No face detected - Relay OFF")

    # Display the frame
    cv2.imshow("Face Detection", frame)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Cleanup GPIO and release resources
GPIO.cleanup()
video.release()
cv2.destroyAllWindows()
