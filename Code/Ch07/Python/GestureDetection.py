import RPi.GPIO as GPIO
import time
import cv2
from cvzone.HandTrackingModule import HandDetector
from picamera2 import Picamera2



ptime = 0
ctime = 0
switch1 = False
switch2 = False
switchpin1 = 26
switchpin2 = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(switchpin1, GPIO.OUT)    # Switch 1
GPIO.setup(switchpin2, GPIO.OUT)    # Switch 2
GPIO.setwarnings(False)

picam2 = Picamera2()
picam2.preview_configuration.main.size = (980,460)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()


detector = HandDetector(detectionCon=0.7, maxHands=1)

while True :
    img= picam2.capture_array()

    hands, img1 = detector.findHands(img)
    
    if hands:
        lmlist = hands[0]
        if lmlist:
            fingerUp = detector.fingersUp(lmlist)
            print(fingerUp)
            if fingerUp == [1, 0, 0, 0, 0] :
                print("Switch 1 toggled")
                if switch1 == False:
                    GPIO.output(switchpin1, GPIO.HIGH)
                    switch1 = True
                else :
                    GPIO.output(switchpin1, GPIO.LOW)
                    switch1 = False
                time.sleep(2)
                
            if fingerUp == [0, 1, 0, 0, 0] :
                print("Switch 2 toggled")
                if switch2 == False:
                    GPIO.output(switchpin2, GPIO.HIGH)
                    switch2 = True
                else :
                    GPIO.output(switchpin2, GPIO.LOW)
                    switch2 = False
                time.sleep(2)
        
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    
    cv2.putText(img, str(f'fps:{int(fps)}'),(5,30), cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),1)
    cv2.imshow("Camera", img)
    if cv2.waitKey(1) & 0xFF==27 :
        break

GPIO.cleanup()
    
cv2.destroyAllWindows()
