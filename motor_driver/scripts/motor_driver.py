#!/usr/bin/env python
# Software License Agreement (BSD License)

import rospy
import socket
import threading
import struct
from std_msgs.msg import Bool
from std_msgs.msg import Float32

class MotorDriver:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.motor_left = ( rospy.get_param('~left/ip','192.168.10.101'), rospy.get_param(rospy.get_name()+'~left/port',4001) )
        self.motor_right = ( rospy.get_param('~right/ip','192.168.10.100'), rospy.get_param(rospy.get_name()+'~right/port',4001) )
        self.left_pwm = 0
        self.right_pwm = 0
        self.is_stop = False
        self.is_end = False
        rospy.Subscriber('~left/duty', Float32, self.callback_left)
        rospy.Subscriber('~right/duty', Float32, self.callback_right)

    def end(self):
        self.is_stop = True
        self.sock.sendto(bytearray(struct.pack("f", 0.)), self.motor_left )
        self.sock.sendto(bytearray(struct.pack("f", 0.)), self.motor_right )

    def callback_left(self, data):
        if data.data > 0.99:
            data.data = 0.99
        elif data.data < -0.99:
            data.data = -0.99
        self.left_pwm = data.data
        if not self.is_stop:
            self.sock.sendto(bytearray(struct.pack("f", self.left_pwm)),  self.motor_left )

    def callback_right(self, data):
        if data.data > 0.99:
            data.data = 0.99
        elif data.data < -0.99:
            data.data = -0.99
        self.right_pwm = data.data
        if not self.is_stop:
            self.sock.sendto(bytearray(struct.pack("f", self.right_pwm)), self.motor_right )

    def callback_stop(data):
        self.is_stop = data.data
        if self.is_stop:
            self.sock.sendto(bytearray(struct.pack("f", 0.)), self.motor_left )
            self.sock.sendto(bytearray(struct.pack("f", 0.)), self.motor_right )
        else:
            self.sock.sendto(bytearray(struct.pack("f", self.left_pwm)),  self.motor_left )
            self.sock.sendto(bytearray(struct.pack("f", self.right_pwm)), self.motor_right )

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
