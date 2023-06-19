#!/usr/bin/env python

# Imports
from niryo_robot_python_ros_wrapper.ros_wrapper import *
import numpy as np
import random
import wandb
import os
import scipy.stats

class NiryoRosWrapperMygym(NiryoRosWrapper):

    def __init__(self, dummy_env, task, sampling_area, eval_steps):
        super(NiryoRosWrapperMygym, self).__init__()

        self.dummy_env = dummy_env
        self.task = task
        self.sampling_area = sampling_area
        self.max_steps = eval_steps
        self.setup_reward()
        self.reset()

    def setup_reward(self):
        if self.task == 'reach':
            self.reward = ReachReward(self)
        elif self.task == 'pnp':
            self.reward = PnPReward(self)
        elif self.task == 'push':
            self.reward = PushReward(self)

    def reset(self):
        self.object_xyz = self.get_center_object_position(self.sampling_area)
        self.target_xyz = self.get_random_object_position(self.sampling_area)
        self.reward.reset()
        self.episode_steps = 0
        self.episode_reward = 0
        self.episode_reward_list = []
        obs_joints = [0, 0, 0, 0, -1.57, 0]
        self.move_joints(*obs_joints)
        if self.task == 'pnp':
            self.gripper_active = False
            self.pnp_finish = False
        observation = self.get_observation()
        print("init observation:{}".format(observation))
        return observation
    
    def get_random_object_position(self, boarders):
        if any(isinstance(i, list) for i in boarders):
            boarders = boarders[random.randint(0,len(boarders)-1)]
        pos = []
        pos.append(random.uniform(boarders[0], boarders[1])) #x
        pos.append(random.uniform(boarders[2], boarders[3])) #y
        pos.append(random.uniform(boarders[4], boarders[5])) #z
        return pos
    
    def get_center_object_position(self, boarders):
        pos = [(boarders[0]+boarders[1])/2, (boarders[2]+boarders[3])/2, (boarders[4]+boarders[5])/2]
        return pos

    # def generate_random_range(self, low, high):
    #     # create random action
    #     result = np.zeros(len(low))
    #     for i in range(len(low)):
    #         result[i] = np.random.uniform(low[i], high[i], 1)
    #     return result

    def step(self, action):
        self.episode_steps += 1
        scaled_action = np.clip(action, self.dummy_env.action_space.low, self.dummy_env.action_space.high)
        # print("act:{}".format(scaled_action))
        self.move_joints(*scaled_action)
        observation = self.get_observation()
        print("obs:{}".format(observation))
        if self.task == 'pnp':
            self.grasp_object(observation)
        finish = self.get_finish(observation)
        reward = self.reward.compute(observation, scaled_action, finish)
        self.episode_reward += reward
        self.episode_reward_list.append(reward)
        wandb.log({"reward":reward})
        if finish or self.episode_steps == self.max_steps:
            self.episode_iqm_reward = scipy.stats.trim_mean(np.array(self.episode_reward_list), proportiontocut=0.25, axis=None)
            print(self.episode_reward, self.episode_iqm_reward, len(self.episode_reward_list))
            wandb.log({"episode sum reward":self.episode_reward, "episode iqm reward":self.episode_iqm_reward, "episode length":len(self.episode_reward_list)})
        return observation, reward, finish

    def grasp_object(self, observation):
        object_pos = observation[:3]
        target_pos = observation[3:6]
        gripper_pos = observation[6:9]
        close_to_object = True if np.linalg.norm(gripper_pos - np.asarray(object_pos)) <= 0.02 else False
        close_to_target = True if np.linalg.norm(gripper_pos - np.asarray(target_pos)) <= 0.02 else False
        if self.gripper_active is False:
            if close_to_object:
                self.close_gripper() # close gripper
                self.gripper_active = True
            else:
                self.open_gripper() # open gripper
        else:
            if close_to_target:
                self.open_gripper() # open gripper
                self.gripper_active = False
                self.pnp_finish = True
            else:
                self.close_gripper() # close gripper

    def get_observation(self):
        # x, y, z = -y, x, z
        target_xyz = np.array([-self.target_xyz[1], self.target_xyz[0], self.target_xyz[2]])
        tcp_pose = self.get_pose()
        endeff_6d = np.array([-tcp_pose.position.y, tcp_pose.position.x, tcp_pose.position.z, tcp_pose.orientation.x, tcp_pose.orientation.y, tcp_pose.orientation.z, tcp_pose.orientation.w])
        if self.task in ["pnp", "push"]:
            object_found, object_pose, object_shape, object_color = self.detect_object(
                self.workspace, shape = ObjectShape.ANY, color = ObjectColor.ANY)
            if object_found:
                self.object_xyz = np.array([-object_pose.y, object_pose.x, object_pose.z])
            obs = np.concatenate((self.object_xyz, target_xyz, endeff_6d),axis=0)
        else:
            obs = np.concatenate((endeff_6d[:3], target_xyz, endeff_6d),axis=0)
        return obs

    def get_finish(self, observation, threshold=0.02):
        if self.task == "reach":
            distance = calc_distance(observation[6:9], observation[3:6])
            finish = (distance <= threshold)
        elif self.task == "pnp":
            finish = self.pnp_finish
        elif self.task == "push":
            distance = calc_distance(observation[:3], observation[3:6])
            finish = (distance <= threshold)
        return finish
        
def calc_distance(obj1, obj2):
    dist = np.linalg.norm(np.asarray(obj1[:3]) - np.asarray(obj2[:3]))
    return dist

class ReachReward:

    def __init__(self, env):
        self.env = env
        self.prev_action = None
        self.init_distance = None

    def compute(self, observation, action, finish):
        if self.prev_action is None:
            self.prev_action = np.array(action)
        o1 = observation[:3]
        o2 = observation[3:6]
        o3 = observation[6:9]
        a = np.array(action) - self.prev_action
        vec = np.array(o2) - np.array(o3)
        dist = np.linalg.norm(vec)
        if self.init_distance is None:
            self.init_distance = dist
        reward_dist = (-1)*(dist/self.init_distance)
        reward_ctrl = (-0.1)*np.square(a).sum()
        collision = self.env.get_collision()
        reward_coll = (-1)*collision
        if finish:
            reward = 10
            print("achieved!!! reward: sum {}".format(reward))
        else:
            reward = reward_dist + reward_ctrl + reward_coll
            print("not achieved... reward: dist {}, ctrl {}, coll {}, finished {}, sum {}".format(reward_dist, reward_ctrl, reward_coll, finish, reward))
        self.prev_action = np.array(action)
        return reward
    
    def reset(self):
        self.prev_action = None
        self.init_distance = None
    
class PnPReward:

    def __init__(self, env):
        self.env = env
        self.prev_action = None
        self.init_distance_1 = None
        self.init_distance_2 = None
    
    def compute(self, observation, action, finish):

        if self.prev_action is None:
            self.prev_action = np.array(action)
        o1 = observation[:3]
        o2 = observation[3:6]
        o3 = observation[6:9]
        a = np.array(action) - self.prev_action
        vec_1 = np.array(o1) - np.array(o3)
        vec_2 = np.array(o2) - np.array(o3)
        dist_1 = np.linalg.norm(vec_1)
        dist_2 = np.linalg.norm(vec_2)
        reward_ctrl = (-0.1)*np.square(a).sum()
        collision = self.env.get_collision()
        reward_coll = (-1)*collision
        if finish:
            reward = 100
            print("achieved!!! reward: sum {}".format(reward))
        elif self.gripper_active:
            if self.init_distance_2 is None:
                self.init_distance_2 = dist_2
            reward_dist = (-1)*(dist_2/self.init_distance_2)
            reward = reward_dist + reward_ctrl + reward_coll + 2
            print("grasped... reward: dist {}, ctrl {}, coll {}, grip {}, finished {}, sum {}".format(reward_dist, reward_ctrl, reward_coll, self.gripper_active, finish, reward))
        else:
            if self.init_distance_1 is None:
                self.init_distance_1 = dist_1
            reward_dist = (-1)*(dist_1/self.init_distance_1)
            reward = reward_dist + reward_ctrl + reward_coll
            print("not grasped... reward: dist {}, ctrl {}, coll {}, grip {}, finished {}, sum {}".format(reward_dist, reward_ctrl, reward_coll, self.gripper_active, finish, reward))
        self.prev_action = np.array(action)
        return reward
    
    def reset(self):

        self.prev_action = None
        self.init_distance_1 = None
        self.init_distance_2 = None

class PushReward:

    def __init__(self, env):
        self.env = env
        self.prev_action = None
        # self.prev_o1 = None
        self.init_distance = None
        self.init_near = None

    def compute(self, observation, action, finish):

        if self.prev_action is None:
            self.prev_action = np.array(action)
        o1 = observation[:3]
        o2 = observation[3:6]
        o3 = observation[6:9]
        a = np.array(action) - self.prev_action
        vec = np.array(o1) - np.array(o2)
        dist = np.linalg.norm(vec)
        vecn = np.array(o1) - np.array(o3)
        near = np.linalg.norm(vecn)
        if self.init_distance is None:
            self.init_distance = dist
        reward_dist = (-1)*(dist/self.init_distance)
        if self.init_near is None:
            self.init_near = near
        reward_near = (-1)*(near/self.init_near)
        # if self.prev_o1 != o1 and self.prev_o1 is not None:
        #     reward_change = 1
        # else:
        #     reward_change = 0
        reward_ctrl = (-0.1)*np.square(a).sum()
        collision = self.env.get_collision()
        reward_coll = (-1)*collision
        if finish:
            reward = 100
            print("achieved!!! reward: sum {}".format(reward))
        else:
            reward = reward_dist + reward_ctrl + reward_coll + reward_near
            # reward = reward_dist + reward_ctrl + reward_coll + reward_change
            print("not achieved... reward: dist {}, ctrl {}, coll {}, near {}, finished {}, sum {}".format(reward_dist,reward_ctrl,reward_coll,reward_near,finish,reward))
        self.prev_action = np.array(action)
        # self.prev_o1 = o1
        return reward

    def reset(self):
        self.prev_action = None
        # self.prev_o1 = None
        self.init_distance = None
        self.init_near = None