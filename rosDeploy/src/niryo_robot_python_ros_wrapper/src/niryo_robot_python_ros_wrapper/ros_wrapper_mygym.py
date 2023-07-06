#!/usr/bin/env python

# Imports
from niryo_robot_python_ros_wrapper.ros_wrapper import *
import numpy as np
import math
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
        if self.task in ['reach','push']:
            self.close_gripper()
        if self.task == 'pnp':
            self.open_gripper()
            self.gripper_active = False
            self.pnp_finish = False
        observation = self.get_observation()
        # print("init observation:{}".format(observation))
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
        # print("obs:{}".format(observation))
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
        close_to_object = True if np.linalg.norm(gripper_pos - np.asarray(object_pos)) <= 0.05 else False
        close_to_target = True if np.linalg.norm(gripper_pos - np.asarray(target_pos)) <= 0.05 else False
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
        endeff_pos = np.array([-tcp_pose.position.y, tcp_pose.position.x, tcp_pose.position.z])
        endeff_ori = np.array([tcp_pose.orientation.w, tcp_pose.orientation.x, tcp_pose.orientation.y, tcp_pose.orientation.z])
        gripper_pos, gripper_ori = self.get_ned2_gripper(endeff_pos,endeff_ori)
        if self.task in ["pnp", "push"]:
            object_found, object_pose, object_shape, object_color = self.detect_object(
                self.workspace, shape = ObjectShape.ANY, color = ObjectColor.ANY)
            if object_found:
                self.object_xyz = np.array([-object_pose.y, object_pose.x, object_pose.z])
            obs = np.concatenate((self.object_xyz, target_xyz, gripper_pos, gripper_ori),axis=0)
        else:
            obs = np.concatenate((gripper_pos, target_xyz, gripper_pos, gripper_ori),axis=0)
        return obs

    def get_ned2_gripper(self, endeff_pos, endeff_ori):
        """
        Returns the position of the tip of the pointy gripper. Tested on Ned2 only
        """
        ori_matrix = quaternion_to_matrix(endeff_ori)
        direction_vector = Vector([0,0,0], [0.075, 0.0, 0.0])
        direction_vector.rotate_with_matrix(ori_matrix)
        gripper = Vector([0,0,0], endeff_pos)
        gripper_pos = direction_vector.add_vector(gripper)
        return gripper_pos, endeff_ori
    
    def get_finish(self, observation, threshold=0.05):
        if self.task == "reach":
            distance = calc_distance(observation[6:9], observation[3:6])
            finish = (distance <= threshold)
        elif self.task == "pnp":
            finish = self.pnp_finish
        elif self.task == "push":
            distance = calc_distance(observation[:3], observation[3:6])
            finish = (distance <= threshold)
        return finish

def quaternion_to_matrix(q):
    """Converts a quaternion to a rotation matrix."""
    q = np.array(q)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    matrix = np.array([
        [1 - 2 * (y**2 + z**2), 2 * (x*y - w*z), 2 * (x*z + w*y)],
        [2 * (x*y + w*z), 1 - 2 * (x**2 + z**2), 2 * (y*z - w*x)],
        [2 * (x*z - w*y), 2 * (y*z + w*x), 1 - 2 * (x**2 + y**2)]
    ])
    return matrix

def calc_distance(obj1, obj2):
    dist = np.linalg.norm(np.asarray(obj1[:3]) - np.asarray(obj2[:3]))
    return dist

class Vector:

    def __init__(self, beginning, end):
        self.beginning = beginning
        self.end = end
        self.vector = self.move_to_origin([beginning, end])
        self.norm = self.count_norm()
        self.normalized = self.get_normalized()

    ### self modifiers:

    def set_len(self, len):
        self.multiply(1 / self.norm)
        self.multiply(len)

    def multiply(self, multiplier):
        self.vector = np.array(self.vector) * multiplier

    def count_norm(self):
        return math.sqrt(np.dot(self.vector, self.vector))

    def get_normalized(self):
        if self.norm == 0:
            return 0
        return self.vector * (1 / self.norm)

    def normalize(self):
        self.vector = self.multiply_vector(self.vector, 1 / self.norm)

    def move_to_origin(self, vector):
        a = vector[1][0] - vector[0][0]
        b = vector[1][1] - vector[0][1]
        c = vector[1][2] - vector[0][2]
        return np.array([a, b, c])

    def visualize(self, origin=[0, 0, 0], color=(0, 0, 0), time=0.1, env=None):
        env.p.addUserDebugLine(origin, np.add(np.array(origin), np.array(self.vector)), lineColorRGB=color,
                                    lineWidth=1, lifeTime=time)

    def add(self, v2):
        r = []
        for i in range(len(self.vector)):
            r.append(self.vector[i] + v2.vector[i])
        self.vector = r

    def rotate_with_matrix(self, matrix):
        self.vector = matrix.dot(self.vector)

        ### interactive:

    def add_vector(self, v2):
        r = []
        for i in range(len(self.vector)):
            r.append(self.vector[i] + v2.vector[i])

        return r

    def get_dot_product(self, v2):
        product = 0
        for i in range(len(self.vector)):
            product += self.vector[i] * v2.vector[i]
        return product

    def get_align(self, v2):
        align = 0
        for i in range(len(self.normalized)):
            align += self.normalized[i] * v2.normalized[i]
        return align
    
class ReachReward:

    def __init__(self, env):
        self.env = env
        self.prev_action = None
        self.init_distance = None

    def compute(self, observation, action, finish):
        o1 = observation[:3]
        o2 = observation[3:6]
        o3 = observation[6:9]
        goal_dist = np.linalg.norm(np.array(o2)-np.array(o3)) # o2-o3
        reward_reach = 0.2*(1-np.tanh(10*goal_dist))
        reward_success = 13 if goal_dist < 0.05 else 0
        collision = self.env.get_collision()
        reward = max(reward_reach, reward_success) + (-0.1*collision)
        # print(f"reward:{reward_reach, reward_success}")
        return reward
    
    def reset(self):
        self.prev_action = None
        self.init_distance = None
    
class PnPReward:

    def __init__(self, env):
        self.env = env
    
    def compute(self, observation, action, finish):
        o1 = observation[:3]
        o2 = observation[3:6]
        o3 = observation[6:9]
        target_dist = np.linalg.norm(np.array(o1)-np.array(o3)) # o1-o2
        goal_dist = np.linalg.norm(np.array(o2)-np.array(o3)) # o2-o3
        reward_reach = 0.2*(1-np.tanh(10*target_dist))
        reward_approach = 0.3+0.4*(1-np.tanh(5*goal_dist)) if self.gripper_active else 0
        reward_success = 45 if finish else 0
        collision = self.env.get_collision()
        reward = max(reward_reach, reward_approach, reward_success) + (-0.1*collision)
        # print(f"reward:{reward_reach, reward_approach, reward_success}")
        return reward
    
    def reset(self):
        pass

class PushReward:

    def __init__(self, env):
        self.env = env
        self.prev_o1 = None

    def compute(self, observation, action, finish):
        o1 = observation[:3]
        if self.pre_o1 == None:
            self.pre_o1 = o1
        o2 = observation[3:6]
        o3 = observation[6:9]
        target_dist = np.linalg.norm(np.array(o1)-np.array(o3)) # o1-o2
        goal_dist = np.linalg.norm(np.array(o1)-np.array(o2)) # o1-o3
        change = 1 if np.linalg.norm(np.array(self.pre_o1) - np.array(o1)) > 0.01 else 0
        reward_reach = 0.2*(1-np.tanh(10*target_dist))
        reward_approach = 0.3+0.4*(1-np.tanh(5*goal_dist)) if target_dist < 0.05 else 0
        reward_success = 45 if goal_dist < 0.05 else 0
        collision = self.env.get_collision()
        reward = max(reward_reach, reward_approach, reward_success) + (-0.1*collision + 1*change)
        # print(f"reward:{reward_reach, reward_approach, reward_success},collision:{collision},change:{change}")
        self.prev_o1 = o1
        return reward

    def reset(self):
        self.prev_o1 = None