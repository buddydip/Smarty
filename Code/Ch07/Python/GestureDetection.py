import RPi.GPIO as GPIO
import time
import cv2
from cvzone.HandTrackingModule import HandDetector

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)    # Switch 1
GPIO.setup(12, GPIO.OUT)    # Switch 2
GPIO.setwarnings(False)

ptime = 0
ctime = 0
switch1 = False
switch2 = False

detector = HandDetector(detectionCon=0.7, maxHands=1)

video = cv2.VideoCapture(0)
video.set(3, 640)
video.set(4, 480)

while True :
    success, img = video.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    
    if hands:
        lmlist = hands[0]
        if lmlist:
            fingerUp = detector.fingersUp(lmlist)
            print(fingerUp)
            if fingerUp == [1, 0, 0, 0, 0] :
                print("Switch 1 toggled")
                if switch1 == False:
                    GPIO.output(11, GPIO.HIGH)
                    switch1 = True
                else :
                    GPIO.output(11, GPIO.LOW)
                    switch1 = False
                time.sleep(2)
                
            if fingerUp == [0, 1, 0, 0, 0] :
                print("Switch 2 toggled")
                if switch2 == False:
                    GPIO.output(12, GPIO.HIGH)
                    switch2 = True
                else :
                    GPIO.output(12, GPIO.LOW)
                    switch2 = False
                time.sleep(2)
        
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    
    cv2.putText(img, str(f'fps:{int(fps)}'),(5,30), cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),1)
    cv2.imshow("Video", img)
    
    if cv2.waitKey(1) & 0xFF==27 :
        break

GPIO.cleanup()
    
video.release()
cv2.destroyAllWindows()
