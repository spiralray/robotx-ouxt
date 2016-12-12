#include <iostream>

#include <ros/ros.h>
#include <std_msgs/Float32.h>
#include <geometry_msgs/Twist.h>
#include <tf/tfMessage.h>

ros::Publisher motor_left, motor_right;

void callback(const geometry_msgs::Twist& twist){
  std_msgs::Float32 left_msg, right_msg;
  left_msg.data = std::min(twist.linear.x/3.0f, 0.7);
  right_msg.data = std::min(twist.linear.x/3.0f, 0.7);
  left_msg.data = std::min(left_msg.data-twist.angular.z, 0.99);
  right_msg.data = std::min(right_msg.data+twist.angular.z, 0.99);
  motor_left.publish(left_msg);
  motor_right.publish(right_msg);
}

int main(int argc, char *argv[]){
  //init the ROS node
  ros::init(argc, argv, "ouxt_base_controller");
  ros::NodeHandle nh;
  motor_left = nh.advertise<std_msgs::Float32>("/motor_left/duty", 10);
  motor_right = nh.advertise<std_msgs::Float32>("/motor_right/duty", 10);
  ros::Subscriber sub = nh.subscribe("cmd_vel", 1, callback);
  ros::spin();
  return 0;
}
