#!/usr/bin/env python

import rospy
import tf2_ros
import tf2_geometry_msgs
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
    twist = Twist()

    if goal is None:
        twist.linear.x = 0
        twist.angular.z = 0
    else:
        try:
            transform = tf_buffer.lookup_transform("base_link", goal.header.frame_id, rospy.Time(0), rospy.Duration(1.0))
            goal_local = tf2_geometry_msgs.do_transform_pose(goal, transform)

            #print(goal_local.pose.position)
            #yaw = tf2_ros.transformations.euler_from_quaternion([goal_local.pose.orientation.x, goal_local.pose.orientation.y, goal_local.pose.orientation.z, goal_local.pose.orientation.w])[2]
            #print(yaw)
            goal_dist = math.sqrt( math.pow(goal_local.pose.position.x, 2) + math.pow(goal_local.pose.position.y, 2) )
            goal_yaw = math.atan2(goal_local.pose.position.y, goal_local.pose.position.x)
            print(goal_dist)
            print(goal_yaw)
            print("")
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
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            print(e)
            twist.linear.x = 0
            twist.angular.z = 0
    vel_pub.publish(twist)

if __name__ == '__main__':
    rospy.init_node('manual',anonymous=True)
    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)
    vel_pub = rospy.Publisher('cmd_vel',Twist, queue_size=1)
    goal_sub = rospy.Subscriber("/move_base_simple/goal", PoseStamped, goalCallback)
    rospy.Timer(rospy.Duration(0.1), timerCallback)
    rospy.spin()
