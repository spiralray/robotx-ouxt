#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import sys

def callback(data):
    twist = Twist()
    mode = Int32()

    twist.linear.x = 2.4*data.axes[1]
    twist.angular.z = data.axes[0]
    vel_pub.publish(twist)

    if data.buttons[7]:
        mode = 1
        mode_pub.publish(mode)
    elif data.buttons[6]:
        mode = 0
        mode_pub.publish(mode)

if __name__ == '__main__':
    rospy.init_node('manual',anonymous=True)
    vel_pub = rospy.Publisher('cmd_vel',Twist, queue_size=1)
    mode_pub = rospy.Publisher('mode',Int32, queue_size=1)
    joy_sub = rospy.Subscriber("joy", Joy, callback)
    rospy.spin()
