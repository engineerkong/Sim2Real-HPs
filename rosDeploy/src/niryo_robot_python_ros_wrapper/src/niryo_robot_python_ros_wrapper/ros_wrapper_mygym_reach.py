#!/usr/bin/env python

# Imports
from niryo_robot_python_ros_wrapper.ros_wrapper import *
import numpy as np
import wandb
import os
import scipy.stats

class NiryoRosWrapperMygym(NiryoRosWrapper):

    def __init__(self, env, model, num_episodes, num_steps, threshold):
        super(NiryoRosWrapperMygym, self).__init__()

        self.env = env
        self.model = model
        self.num_episodes = num_episodes
        self.num_steps = num_steps
        self.threshold = threshold
        self.target_xyz = np.array([0.5, 0.0, 0.0])
        self.prev_action = None
        self.reset()

    def reset(self):
        self.prev_obj1_position = None
        self.prev_obj2_position = None
        self.done = False
        self.episode_reward_list = []
        obs_joints = [0, 0, 0, 0, 0, 0]
        self.move_joints(*obs_joints)
        self.get_observation()

    def generate_random_range(self, low, high):
        result = np.zeros(len(low))
        for i in range(len(low)):
            result[i] = np.random.uniform(low[i], high[i], 1)
        return result
            
    def test(self):
        self.obs = [-1.0228927688002336e-08, 0.24520003516036062, 0.38804871518259465, -0.14393927545798518, 0.33133210103521077, 0.1, 
                    -1.0228927688002336e-08, 0.24520003516036062, 0.38804871518259465]
        print("obs:{}".format(self.obs))
        self.action, self._states = self.model.predict(self.obs)
        print("action:{}".format(self.action))

    def eval(self):
        with wandb.init(
            mode="offline",
            project="ros_test_seeds",
            dir=os.getcwd()
        ):
            for i in range(self.num_episodes):
                episode_reward = 0
                self.reset()
                print("init observation:{}".format(self.obs))
                for j in range(self.num_steps):
                    print("steps:{}".format(j))
                    # self.action = self.generate_random_range(self.env.action_space.low, self.env.action_space.high)
                    # self.move_pose(0.25, 0.0357, 0.05, 0, 0, 0)
                    # self.action = self.get_joints()
                    self.action, self._states = self.model.predict(self.obs)
                    print("action:{}".format(self.action))                    
                    self.step()
                    joint_state = self.get_joints()
                    print("state:{}".format(joint_state))
                    self.get_observation()
                    print("observation:{}".format(self.obs))
                    self.get_done()
                    self.get_reward()
                    episode_reward += self.reward
                    self.episode_reward_list.append(self.reward)
                    wandb.log({"reward":self.reward})
                    if self.done:
                        break
                self.episode_iqm_reward = scipy.stats.trim_mean(np.array(self.episode_reward_list), proportiontocut=0.25, axis=None)
                wandb.log({"episode iqm reward":self.episode_iqm_reward})
                print("finished... done:{}, episode:{}, steps:{}, episode_reward:{}".format(self.done, i,j,episode_reward))

    def step(self):
        action = np.clip(self.action, self.env.action_space.low, self.env.action_space.high)
        self.move_joints(*action)

    def get_observation(self):

        tcp_pose = self.get_pose()
        self.endeff_xyz_trans = np.array([-tcp_pose.position.y, tcp_pose.position.x, tcp_pose.position.z])
        self.target_xyz_trans = np.array([-self.target_xyz[1], self.target_xyz[0], self.target_xyz[2]])
        self.obs = np.concatenate((self.endeff_xyz_trans, self.target_xyz_trans, self.endeff_xyz_trans),axis=0)

    def get_reward(self):
        
        # self.reward = self.calc_dist_diff(self.endeff_xyz_trans, self.target_xyz_trans) + collision * (-1)
        if self.prev_action is None:
            self.prev_action = np.array(self.action)
        a = np.array(self.action) - self.prev_action
        vec = np.array(self.endeff_xyz_trans) - np.array(self.target_xyz_trans)
        reward_dist = -np.linalg.norm(vec)
        reward_ctrl = -np.square(a).sum()
        collision = self.get_collision()
        if self.done:
            self.reward = reward_dist + 0.1*reward_ctrl + (-1)*collision + 5
        else:
            self.reward = reward_dist + 0.1*reward_ctrl + (-1)*collision
        print("reward: dist {}, ctrl {}, coll {}, finished {}, sum {}".format(reward_dist, 0.1*reward_ctrl, (-1)*collision, self.done, self.reward))

    def get_done(self):

        distance = self.calc_distance(self.endeff_xyz_trans, self.target_xyz_trans)
        if distance <= self.threshold:
            self.done = True
    
    def calc_dist_diff(self, obj1_position, obj2_position):

        if self.prev_obj1_position is None and self.prev_obj2_position is None:
            self.prev_obj1_position = obj1_position
            self.prev_obj2_position = obj2_position
        self.prev_diff = self.calc_distance(self.prev_obj1_position, self.prev_obj2_position)

        current_diff = self.calc_distance(obj1_position, obj2_position)
        norm_diff = (self.prev_diff - current_diff) / self.prev_diff

        self.prev_obj1_position = obj1_position
        self.prev_obj2_position = obj2_position

        return norm_diff

    def calc_distance(self, obj1, obj2):

        dist = np.linalg.norm(np.asarray(obj1[:3]) - np.asarray(obj2[:3]))
        return dist