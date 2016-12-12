#include <iostream>

#include <ros/ros.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Float32.h>
#include <geometry_msgs/Twist.h>
#include <tf/tfMessage.h>

ros::Publisher motor_left, motor_right;

int mode = 0;

void OutputMotor(const geometry_msgs::Twist& twist){
  std_msgs::Float32 left_msg, right_msg;
  left_msg.data = std::min(twist.linear.x/3.0f, 0.7);
  right_msg.data = std::min(twist.linear.x/3.0f, 0.7);
  left_msg.data = std::min(left_msg.data-twist.angular.z/3, 0.99);
  right_msg.data = std::min(right_msg.data+twist.angular.z/3, 0.99);
  motor_left.publish(left_msg);
  motor_right.publish(right_msg);
}

void ManualTwistCallback(const geometry_msgs::Twist& twist){
  if(mode == 0){
    OutputMotor(twist);
  }
}
void AutoTwistCallback(const geometry_msgs::Twist& twist){
  if(mode == 1){
    OutputMotor(twist);
  }
}

void ModeCallback(const std_msgs::Int32& data){
  mode = data.data;
  std_msgs::Float32 msg;
  msg.data = 0;
  motor_left.publish(msg);
  motor_right.publish(msg);
}

int main(int argc, char *argv[]){
  //init the ROS node
  ros::init(argc, argv, "ouxt_base_controller");
  ros::NodeHandle nh;
  motor_left = nh.advertise<std_msgs::Float32>("/motor_left/duty", 10);
  motor_right = nh.advertise<std_msgs::Float32>("/motor_right/duty", 10);
  ros::Subscriber manual_sub = nh.subscribe("manual_vel", 1, ManualTwistCallback);
  ros::Subscriber auto_sub = nh.subscribe("cmd_vel", 1, AutoTwistCallback);
  ros::Subscriber mode_sub = nh.subscribe("mode", 1, ModeCallback);
  ros::spin();
  return 0;
}
