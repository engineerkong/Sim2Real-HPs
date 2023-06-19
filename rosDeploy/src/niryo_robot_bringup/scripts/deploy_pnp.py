#!/usr/bin/env python

from std_srvs.srv import Empty
import rospy

# Initializing ROS node
rospy.init_node('niryo_robot_example_python_ros_wrapper')

reset_proxy = rospy.ServiceProxy("/gazebo/reset_world", Empty)

try:
    reset_proxy()

except rospy.ServiceException as e:
    print("/gazebo/reset_simulation service call failed")