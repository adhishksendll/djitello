from djitellopy import Tello
import KeyPressModule as kp
from time import sleep
import numpy as np
import cv2
import math

########################### PARAMETERS ###############################
fSpeed = 117 / 10  # Forward speed in cm/s
aSpeed = 360 / 10  # Angular speed in deg/s
interval = 0.25    # Time interval in seconds

dInterval = fSpeed * interval  # Distance moved in one interval
aInterval = aSpeed * interval  # Degrees turned in one interval
######################################################################

x, y = 500, 500  # Starting coordinates
yaw = 0          # Initial yaw (heading)
kp.init()

me = Tello()
me.connect()
print("Battery:", me.get_battery())

points = [(x, y)]  # Path points

def getKeyboardInput():
    lr, fb, ud, yw = 0, 0, 0, 0
    speed = 15
    aspeed = 50
    global x, y, yaw

    d = 0
    angle = None

    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        angle = -90
    elif kp.getKey("RIGHT"):
        lr = speed
        d = dInterval
        angle = 90
    elif kp.getKey("UP"):
        fb = speed
        d = dInterval
        angle = 0
    elif kp.getKey("DOWN"):
        fb = -speed
        d = dInterval
        angle = 180

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yw = -aspeed
        yaw -= aInterval
    elif kp.getKey("d"):
        yw = aspeed
        yaw += aInterval

    if kp.getKey("e"):
        me.takeoff()
    elif kp.getKey("q"):
        me.land()

    yaw %= 360  # Keep yaw in 0–359 degrees

    if angle is not None:
        x += int(d * math.cos(math.radians(yaw + angle)))
        y += int(d * math.sin(math.radians(yaw + angle)))

    return [lr, fb, ud, yw, x, y]

def drawPoints(img, points):
    for i in range(1, len(points)):
        cv2.line(img, points[i - 1], points[i], (255, 255, 0), 2)
        cv2.circle(img, points[i], 4, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, points[-1], 6, (0, 255, 0), cv2.FILLED)
    coords = f'({(points[-1][0] - 500) / 100:.1f}, {(points[-1][1] - 500) / 100:.1f}) m'
    cv2.putText(img, coords, (points[-1][0] + 10, points[-1][1] + 30),
                cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 255), 1)

def drawBattery(img, battery):
    cv2.putText(img, f'Battery: {battery}%', (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)

    if points[-1][0] != vals[4] or points[-1][1] != vals[5]:
        points.append((vals[4], vals[5]))

    drawPoints(img, points)
    drawBattery(img, me.get_battery())

    cv2.imshow("Tello Path Visualization", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        me.land()
        break

    sleep(interval)

cv2.destroyAllWindows()
