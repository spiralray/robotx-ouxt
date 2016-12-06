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
        self.motor = ( rospy.get_param('~ip'), rospy.get_param(rospy.get_name()+'~port',4001) )
        self.sock.sendto(bytearray(struct.pack("f", 0.)), self.motor )
        
        self.duty = 0.
        self.is_stop = False
        rospy.Subscriber('~duty', Float32, self.callback)
        rospy.Subscriber('~stop', Float32, self.callback)

    def end(self):
        self.is_stop = True
        self.sock.sendto(bytearray(struct.pack("f", 0.)), self.motor )

    def callback(self, data):
        if data.data > 0.99:
            data.data = 0.99
        elif data.data < -0.99:
            data.data = -0.99
        self.duty = data.data
        if not self.is_stop:
            self.sock.sendto(bytearray(struct.pack("f", self.duty)), self.motor )

    def callback_stop(data):
        self.is_stop = data.data
        if self.is_stop:
            self.sock.sendto(bytearray(struct.pack("f", 0.)), self.motor )
        else:
            self.sock.sendto(bytearray(struct.pack("f", self.duty)), self.motor )

if __name__ == '__main__':
    rospy.init_node('motor_driver', anonymous=False)
    md = MotorDriver()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Motor Driver module"
    finally:
        md.end()
