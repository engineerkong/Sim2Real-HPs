#!/usr/bin/env python

# Imports
from niryo_robot_python_ros_wrapper.ros_wrapper_mygym_reach import *
# from detection_improve import detection_improve
import torch
import functools
from sb3_python2.model import Model
from sb3_python2.policy import MlpPolicy, MultiInputPolicy
from gym.spaces import Box, MultiDiscrete, Dict
import rospy
import numpy as np

def recursive_getattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split("."))

class MygymReachEnv:

    def __init__(self):
        
        self.observation_space = Box(-float('inf'), float('inf'), (9,))
        self.action_space = Box(-float(1), float(1), (6,))
        self.action_space.high = np.array([2.99987191833, 0.610167106497, 1.57009819509, 2.09003177926, 1.92282923692, 2.53002928369])
        self.action_space.low = np.array([-2.99987191833, -1.83259571459, -1.34006379968, -2.09003177926, -1.92003671012, -2.53002928369])

print("---load---")
env = MygymReachEnv()
model = Model(env, MlpPolicy)
params = torch.load('model_torch_reach.pth.tar')
for name in params:
    attr = None
    attr = recursive_getattr(model, name)
    attr.load_state_dict(params[name])

print("---deploy---")
# detection_improve()
rospy.init_node('niryo_robot_example_python_ros_wrapper')
num_episodes, num_steps = 100, 100
threshold = 0.1
ros_robot = NiryoRosWrapperMygym(model, num_episodes, num_steps, threshold)
ros_robot.eval()