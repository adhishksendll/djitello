from djitellopy import tello
import cv2
import numpy as np
import time

me = tello.Tello()
me.connect()
print("Tello Battery Level:", me.get_battery())

me.streamon()
me.takeoff()

time.sleep(2)  # Hover to stabilize
me.send_rc_control(0, 0, 30, 0)
time.sleep(3)  # Gain altitude slightly for better visibility
me.send_rc_control(0, 0, 0, 0)

w, h = 800,600
fbRange = [4000, 6000]  # Adjusted range for better tracking stability
pid = [0.45, 0.4, 0]  # Tuned P and D values
pError = 0

def findFace(img):
    facecascade = cv2.CascadeClassifier("Resources/haarcascade_fullbody")
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = facecascade.detectMultiScale(imggray, 1.2, 8)

    myfacelistc = []
    myfacelistarea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myfacelistc.append([cx, cy])
        myfacelistarea.append(area)

    if myfacelistarea:
        i = myfacelistarea.index(max(myfacelistarea))
        return img, [myfacelistc[i], myfacelistarea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -40, 40))  # Lowered max yaw speed

    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -15
    elif area < fbRange[0] and area != 0:
        fb = 15

    if x == 0:
        speed = 0
        error = 0

    me.send_rc_control(0, fb, 0, speed)

    return error


while True:
    img = cv2.cvtColor(me.get_frame_read().frame, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(info, w, pid, pError)

    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.send_rc_control(0, 0, 0, 0)
        time.sleep(0.5)
        me.land()
        break