#!/usr/bin/env python

from std_srvs.srv import Empty
import rospy
from niryo_robot_python_ros_wrapper.ros_wrapper import *

# Initializing ROS node
rospy.init_node('niryo_robot_example_python_ros_wrapper')
n = NiryoRosWrapper()
# object pos 0.35,0.1,0.012
# # reach example
# n.close_gripper()
# n.move_pose(0.35,0.1,0.12,0,1.57,0)
# pnp example
n.open_gripper()
n.move_pose(0.35,0.1,0.1,0,1.57,0)
n.close_gripper()
n.move_pose(0.15,-0.1,0.11,0,1.57,0)
n.open_gripper()
# push example
# n.close_gripper()
# n.move_pose(0.336,0.15,0.1,0,1,0)
# n.move_pose(0.29,-0.05,0.1,0,1,0)


