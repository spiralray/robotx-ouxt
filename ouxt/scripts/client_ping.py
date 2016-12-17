#!/usr/bin/env python

import rospy

import os
import subprocess
import time

proc_joy = None
proc_heartbeat = None

def check_connection(hostname):
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    if os.environ['ROS_MASTER_URI']:
        ros_master_ip = os.environ['ROS_MASTER_URI'].split(":")[1].replace('/','')
    else:
        ros_master_ip = 'localhost'
    print(ros_master_ip)
    while True:
        connection = check_connection(ros_master_ip)
        if connection:
            if proc_joy is None:
                proc_joy = subprocess.Popen("rosrun joy joy_node",shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            if proc_heartbeat is None:
                proc_heartbeat = subprocess.Popen('rostopic pub /heartbeat std_msgs/Empty "{}" -r5',shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        else:
            print('Server disconnected. Reconnecting...')
            if proc_joy is not None:
                proc_joy.kill()
                proc_joy = None
            if proc_heartbeat is not None:
                proc_heartbeat.kill()
                proc_heartbeat = None
        time.sleep(1)
