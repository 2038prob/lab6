#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt16
import sys, select, os

if os.name == 'nt':
    import msvcrt
else:
    import tty, termios

MAX = 180
MIN = 0

msg = """
Control Your Traxxis!
--------------------------------
Controls:
        w
   a    s    d
        x

w/s : increase/decrease throttle (MIN = 0, MAX = 180)
a/d : increase/decrease steering angle (MIN = 30, MAX = 150)

space key, x : force stop

CTRL-C to quit
"""

def getKey():
    if os.name == 'nt':
      if sys.version_info[0] >= 3:
        return msvcrt.getch().decode()
      else:
        return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def constrain(input, low=MIN, high=MAX):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input
    return input

def pretty(steer, throttle):
    print("currently:\tsteering angle %s\t throttle %s " % (steer, throttle))

if __name__ == "__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('traxxis_teleop')
    pub1 = rospy.Publisher('servo2', UInt16, queue_size=10)
    pub2 = rospy.Publisher('servo1', UInt16, queue_size=10)
    
    count = 0
    steer = 90
    throttle = 90
    
    while(1):
        key = getKey()
        if count % 20 ==0:
            print(msg)
            count += 1
        if key != '':
            count += 1
        if key == 'w':
            print("Key Pressed: " + key)
            throttle = constrain(throttle+30)
            pretty(steer, throttle)
        elif key == 's':
            print("Key Pressed: " + key)
            throttle = constrain(throttle-30)
            pretty(steer, throttle)
        elif key in ['x', ' ']:
            print("Key Pressed: " + key)
            throttle = 90
            pretty(steer, throttle)
        elif key == 'a':
            print("Key Pressed: " + key)
            steer = constrain(steer-30, 30, 150)
            pretty(steer, throttle)
        elif key == 'd':
            print("Key Pressed: " + key)
            steer = constrain(steer+30, 30, 150)
            pretty(steer, throttle)
        else:
            if (key == '\x03'):
                break
        pub1.publish(steer)
        pub2.publish(throttle)
