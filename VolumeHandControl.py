import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#######################################################
wCam, hCam = 460, 480
#######################################################

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
length = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)
minlenght = length[0]
maxlength = length[1]
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
vol = 0
volbar = 0
detector = htm.handDetector(detectionCon=0.7)

while True:
    success, img = cap.read()
    img = detector.findHands(img)

    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1],lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2 , (y1+y2)//2
        cv2.circle(img, (x1,y1), 10, (255,0,0), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,0), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        vol = np.interp(length, [30, 150], [minlenght, maxlength])
        volbar = np.interp(length, [30, 150], [300, 150])
        volume.SetMasterVolumeLevel(vol, None)
        if length < 50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        elif length < 100 and length > 50:
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
        elif length < 150 and length > 100:
            cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)
        elif length < 200 and length > 150:
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

    cv2.rectangle(img,(50, 150), (85, 300), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volbar)), (85, 300), (0, 255, 0), cv2.FILLED)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime


    cv2.putText(img, f"fps: {int(fps)}",(30,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
