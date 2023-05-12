#!/usr/bin/env python

# Imports
from niryo_robot_python_ros_wrapper.ros_wrapper_mygym_reach import *
# from detection_improve import detection_improve
import torch
import functools
# from sb3_py2.ppo_algorithm import PPO
from sb3_py2.sac_algorithm import SAC
# from sb3_py2.ppo_policy import MlpPolicy
from sb3_py2.sac_policy import MlpPolicy
from gym.spaces import Box
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
        # self.action_space.high = np.array([2.98987191833, 0.600167106497, 1.56009819509, 2.08003177926, 1.91282923692, 2.52002928369])
        # self.action_space.low = np.array([-2.98987191833, -1.82259571459, -1.33006379968, -2.08003177926, -1.91003671012, -2.52002928369])
        # actually
        self.action_space.high = np.array([2.99987191833, 0.610167106497, 1.57009819509, 2.09003177926, 1.92282923692, 2.53002928369])
        self.action_space.low = np.array([-2.99987191833, -1.83259571459, -1.34006379968, -2.09003177926, -1.92003671012, -2.53002928369])
        self.reward_range = (-float('inf'), float('inf'))
        self.metadata = {}
        
print("---load---")
env = MygymReachEnv()
model = SAC(MlpPolicy, env)
params = torch.load('./model_torch/model_torch_reach_0505_1.pth.tar')
for name in params:
    attr = None
    attr = recursive_getattr(model, name)
    attr.load_state_dict(params[name])

print("---deploy---")
# detection_improve()
rospy.init_node('niryo_robot_example_python_ros_wrapper')
num_episodes, num_steps = 10, 100
threshold = 0.1
ros_robot = NiryoRosWrapperMygym(model, num_episodes, num_steps, threshold)
ros_robot.test()