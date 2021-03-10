#include "ros/ros.h"
#include "my_id_robot/FindObjectOpenCV.h"
#include "std_msgs/String.h"

#include <cstdlib>

int main(int argc, char **argv)
{
  ros::init(argc, argv, "main_object_client");
  if (argc != 1)
  {
    ROS_INFO("usage: main_object_client");
    return 1;
  }

  ros::NodeHandle n;
  ros::ServiceClient client = n.serviceClient<my_id_robot::FindObjectOpenCV>("my_id_robot");

  ros::Publisher servoControl = n.advertise<std_msgs::String>("servo_control", 100);
  
  my_id_robot::FindObjectOpenCV srv;
  srv.request.id_object = "object";

  std_msgs::String msg;
  std::stringstream ss;

  if (client.call(srv))
  {
    int position = 400;
    
    
    ROS_INFO("X: %d", srv.response.x);
    ROS_INFO("Y: %d", srv.response.y);
    if (srv.response.x > 500)
      ss << "3, " << 300;
    else
      ss << "3, " << 700;
    msg.data = ss.str();
    servoControl.publish(msg);
    ros::spinOnce();
  }
  else
  {
    ROS_ERROR("Failed to call service find_object_opencv");
    return 1;
  }

  return 0;
}
