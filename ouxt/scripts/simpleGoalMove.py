#!/usr/bin/env python

import rospy
import tf
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from math import pi
import math

goal = None

def goalCallback(data):
    global goal
    goal = data
    print(goal)

def timerCallback(event):
    global goal
    global tf_listener
    twist = Twist()

    if goal is None:
        twist.linear.x = 0
        twist.angular.z = 0
    else:
        goal.header.stamp = rospy.Time.now()
        try:
            goal_local = tf_listener.transformPose('/base_link', goal)
            #print(goal_local.pose.position)
            #yaw = tf.transformations.euler_from_quaternion([goal_local.pose.orientation.x, goal_local.pose.orientation.y, goal_local.pose.orientation.z, goal_local.pose.orientation.w])[2]
            #print(yaw)
            goal_dist = math.sqrt( math.pow(goal_local.pose.position.x, 2) + math.pow(goal_local.pose.position.y, 2) )
            goal_yaw = math.atan2(goal_local.pose.position.y, goal_local.pose.position.x)
            if goal_dist <= 3:
                twist.linear.x = 0
                twist.angular.z = 0
            else:
                if math.fabs(goal_yaw) < pi/4:
                    twist.linear.x = goal_dist
                    twist.angular.z = goal_yaw
                else:
                    twist.linear.x = 0
                    twist.angular.z = goal_yaw
            print(goal_dist)
            print(goal_yaw)
            print("")
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logdebug("LookupException")
            twist.linear.x = 0
            twist.angular.z = 0
    vel_pub.publish(twist)

if __name__ == '__main__':
    rospy.init_node('manual',anonymous=True)
    tf_listener = tf.TransformListener()
    vel_pub = rospy.Publisher('cmd_vel',Twist, queue_size=1)
    goal_sub = rospy.Subscriber("/move_base_simple/goal", PoseStamped, goalCallback)
    rospy.Timer(rospy.Duration(0.1), timerCallback)
    rospy.spin()
