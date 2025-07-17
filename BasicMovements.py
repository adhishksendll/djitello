from djitellopy import tello
from time import sleep

me = tello.Tello()
me.connect()
print("Tello Battery Level:",me.get_battery())

me.takeoff()

me.send_rc_control(0,0,0,100)
sleep(3)
me.send_rc_control(0,0,0,0)
sleep(2)
me.land()