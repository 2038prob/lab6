#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16

def servo_sweep():

    rospy.init_node('servo_node', anonymous=True)
    pub = rospy.Publisher('servo', UInt16, queue_size=10)

    #r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        # From 0 to 180 degrees
        for angle in range(0,180):
            pub.publish(angle)
            rospy.sleep(0.005)
        # From 180 to 0 degrees
        for angle in range(180,-1,-1):
            pub.publish(angle)
            rospy.sleep(0.005)
        #r.sleep()

def steer_callback(value):
    rospy.init_node('steer_node', anonymous=True)
    pub = rospy.Publisher('servo1', UInt16, queue_size=10)
    

def throttle_callback(value):
    rospy.init_node('throttle_node', anonymous=True)
    pub = rospy.Publisher('servo2', UInt16, queue_size=10)
    

def listener():
    topic1 = "servo1" # Steer
    topic2 = "servo2" # Throttle
    rospy.Subscriber(topic1, UInt16, steer_callback) # listen to teleop
    rospy.Subscriber(topic2, UInt16, throttle_callback) # listen to teleop
    

if __name__ == '__main__':
    try:
        while rospy.is_shutdown:
            listener()
    except rospy.ROSInterruptException:
        pass
