from djitellopy import tello
import cv2

me = tello.Tello()
me.connect()
print("Tello Battery Level:",me.get_battery())

me.streamon()

while True:
    img = me.get_frame_read().frame
    #img = cv2.resize(img,(368,248))
    cv2.imshow("Image", img)
    cv2.waitKey(1)