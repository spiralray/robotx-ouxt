#!/usr/bin/env python

import rospy
from std_msgs.msg import Empty
from std_msgs.msg import Bool
import sys

heartbeat = 0

def callback(data):
    global heartbeat
    heartbeat = 5
    msg = Bool()
    msg.data = False
    stop_pub.publish(msg)

def timerCallback(event):
    global heartbeat
    global right_pub, left_pub
    if heartbeat <= 0:
        msg = Bool()
        msg.data = True
        stop_pub.publish(msg)
        print("HeartBeat Timeout")
    else:
        heartbeat -= 1


if __name__ == '__main__':
    rospy.init_node('heartbeat',anonymous=True)
    stop_pub = rospy.Publisher('/stop',Bool, queue_size=1)
    rospy.Subscriber('heartbeat', Empty, callback)
    rospy.Timer(rospy.Duration(1), timerCallback)
    rospy.spin()
