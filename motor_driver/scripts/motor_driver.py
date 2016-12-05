#!/usr/bin/env python
# Software License Agreement (BSD License)

import rospy
import socket
import threading
from std_msgs.msg import Bool
from std_msgs.msg import Float64

class MotorDriver:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.motor_left = ( rospy.get_param(rospy.get_name()+'/left/ip','192.168.10.101'), rospy.get_param(rospy.get_name()+'/left/port',4001) )
        self.motor_right = ( rospy.get_param(rospy.get_name()+'/right/ip','192.168.10.100'), rospy.get_param(rospy.get_name()+'/right/port',4001) )
        self.left_pwm = 0
        self.right_pwm = 0
        self.is_stop = False
        self.is_end = False
        self.update()

    def update(self):
        if self.is_stop:
            self.sock.sendto("0", self.motor_left )
            self.sock.sendto("0", self.motor_right )
        else:
            self.sock.sendto("{0:.3f}".format(self.left_pwm),  self.motor_left )
            self.sock.sendto("{0:.3f}".format(self.right_pwm), self.motor_right )
        if not self.is_end:
            self.timer = threading.Timer(0.05, self.update)
            self.timer.start()

    def end(self):
        self.is_stop = True
        if self.timer.is_alive():
            self.timer.cancel()
        self.update()

    def callback_left(self, data):
        if data.data > 1:
            data.data = 1
        elif data.data < -1:
            data.data = -1
        self.left_pwm = data.data

    def callback_right(self, data):
        if data.data > 1:
            data.data = 1
        elif data.data < -1:
            data.data = -1
        self.right_pwm = data.data

    def callback_stop(data):
        self.is_stop = data.data

if __name__ == '__main__':
    rospy.init_node('motor_driver', anonymous=False)
    md = MotorDriver()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Motor Driver module"
    finally:
        md.is_end = True
        md.end()
