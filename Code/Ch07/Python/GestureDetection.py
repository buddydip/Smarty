import RPi.GPIO as GPIO
import time
import cv2
from cvzone.HandTrackingModule import HandDetector
from picamera2 import Picamera2


import json
import paho.mqtt.client as mqtt


MQTT_ADDRESS:str = 'smarty.local'
MQTT_TOPIC_SWITCH: str = 'smarty/switchcontrol/mainstudy'
MQTT_CLIENT_ID:str = 'MQTTDataBridge'
MQTT_PORT:int = 1883

switchID1 = 'MAINSTUDY.Switch4'
switchID2 = 'MAINSTUDY.Switch3'

    
def _publish_message(topic, switchID, switchState):
    data = {}
    data['SwitchID'] = switchID
    data['SwitchState'] = switchState
    payload = json.dumps(data)
    print(payload)
    mqtt_client.publish(MQTT_TOPIC_SWITCH, payload)
    return
 


mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
mqtt_client.connect(MQTT_ADDRESS, MQTT_PORT)
mqtt_client.loop_start()  # start the loop


ptime = 0
ctime = 0
switch1 = False
switch2 = False


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
                _publish_message(MQTT_TOPIC_SWITCH, switchID1, not(switch1))
                switch1 = not(switch1)
                time.sleep(2)
                
            if fingerUp == [0, 1, 0, 0, 0] :
                print("Switch 2 toggled")
                _publish_message(MQTT_TOPIC_SWITCH, switchID2, not(switch2))
                switch2 = not(switch2)
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

