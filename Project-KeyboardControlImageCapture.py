from djitellopy import tello
import KeyPressModule as kp
from time import sleep
import time
import cv2

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
global img

me.streamon()

def getKeyboardInput():
    lr, fb, ud, yw = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"): yw = -speed
    elif kp.getKey("d"): yw = speed

    if kp.getKey("e"):
        me.takeoff()

    if kp.getKey("q"):
        me.land()

    if kp.getKey("f"):
        cv2.imwrite(f'Resources/Images{time.time()}.jpg')
        sleep(0.3)

    return [lr, fb, ud, yw]

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame
    img = cv2.resize(img,(368,248))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
