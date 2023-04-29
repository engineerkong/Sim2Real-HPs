#!/usr/bin/env python

# Imports
from niryo_robot_python_ros_wrapper.ros_wrapper import *
import numpy as np

class NiryoRosWrapperMygym(NiryoRosWrapper):

    def __init__(self, model, num_episodes, num_steps, threshold):
        super(NiryoRosWrapperMygym, self).__init__()

        self.model = model
        self.num_episodes = num_episodes
        self.num_steps = num_steps
        self.threshold = threshold
        self.target_xyz = np.array([0.1, 0.3, 0.1])

        self.reset()

    def reset(self):
        self.prev_obj1_position = None
        self.prev_obj2_position = None
        self.done = False
        obs_joints = [0, 0.4, -0.4, 0, -1.57, 0]
        self.move_joints(*obs_joints)
        self.get_observation()
    
    def eval(self):
        for i in range(self.num_episodes):
            episode_reward = 0
            self.reset()
            for j in range(self.num_steps):
                self.action, self._states = self.model.predict(self.obs)
                self.step()
                self.get_observation()
                self.get_reward()
                self.get_done()
                episode_reward += self.reward
                if self.done:
                    print("done!!! episode:{}, steps:{}, episode_reward:{}".format(i,j,episode_reward))
            if not self.done:
                print("not done... episode:{}, steps:{}, episode_reward:{}".format(i,j,episode_reward))

    def step(self):
        print(self.action)
        self.move_joints(*self.action)

    def get_observation(self):

        tcp_pose = self.get_pose()
        self.endeff_xyz = np.array([tcp_pose.position.x, tcp_pose.position.y, tcp_pose.position.z])
        self.obs = np.concatenate((self.endeff_xyz, self.target_xyz, self.endeff_xyz),axis=0)

    def get_reward(self):

        self.reward = self.calc_dist_diff(self.endeff_xyz, self.target_xyz)

    def get_done(self):

        distance = self.calc_distance(self.endeff_xyz, self.target_xyz)
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