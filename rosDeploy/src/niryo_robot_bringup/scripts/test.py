#!/usr/bin/env python

from std_srvs.srv import Empty
import rospy
from niryo_robot_python_ros_wrapper.ros_wrapper import *

# Initializing ROS node
rospy.init_node('niryo_robot_example_python_ros_wrapper')
n = NiryoRosWrapper()
n.move_pose(0.25,0,0.012,0,0,0)
print(n.get_pose())


