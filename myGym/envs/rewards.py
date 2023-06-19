import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3.common import results_plotter
import os
import math
from math import sqrt
from myGym.utils.vector import Vector
import random

class Reward:
    """
    Reward base class for reward signal calculation and visualization

    Parameters:
        :param env: (object) Environment, where the training takes place
        :param task: (object) Task that is being trained, instance of a class TaskModule
    """
    def __init__(self, env, task=None):
        self.env = env
        self.task = task
        self.rewards_history = []
        self.current_network = 0
        self.num_networks = env.num_networks
        #self.check_num_networks()
        self.network_rewards = [0] * self.num_networks

    def network_switch_control(self, observation):
        if self.env.num_networks <= 1:
            print("Cannot switch networks in a single-network scenario")
        else:
           if self.env.network_switcher == "gt":
                self.current_network = self.decide(observation)
           else:
               raise NotImplementedError("Currently only implemented ground truth ('gt') network switcher")
        return self.current_network

    def compute(self, observation=None):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def visualize_reward_over_steps(self):
        """
        Plot and save a graph of reward values assigned to individual steps during an episode. Call this method after the end of the episode.
        """
        save_dir = os.path.join(self.env.logdir, "rewards")
        os.makedirs(save_dir, exist_ok=True)
        if self.env.episode_steps > 0:
            results_plotter.EPISODES_WINDOW=50
            results_plotter.plot_curves([(np.arange(self.env.episode_steps),np.asarray(self.rewards_history[-self.env.episode_steps:]))],'step','Step rewards')
            plt.ylabel("reward")
            plt.gcf().set_size_inches(8, 6)
            plt.savefig(save_dir + "/reward_over_steps_episode{}.png".format(self.env.episode_number))
            plt.close()

    def visualize_reward_over_episodes(self):
        """
        Plot and save a graph of cumulative reward values assigned to individual episodes. Call this method to plot data from the current and all previous episodes.
        """
        save_dir = os.path.join(self.env.logdir, "rewards")
        os.makedirs(save_dir, exist_ok=True)
        if self.env.episode_number > 0:
            results_plotter.EPISODES_WINDOW=10
            results_plotter.plot_curves([(np.arange(self.env.episode_number),np.asarray(self.env.episode_final_reward[-self.env.episode_number:]))],'episode','Episode rewards')
            plt.ylabel("reward")
            plt.gcf().set_size_inches(8, 6)
            plt.savefig(save_dir + "/reward_over_episodes_episode{}.png".format(self.env.episode_number))
            plt.close()


class DistanceReward(Reward):
    """
    Reward class for reward signal calculation based on distance differences between 2 objects

    Parameters:
        :param env: (object) Environment, where the training takes place
        :param task: (object) Task that is being trained, instance of a class TaskModule
    """
    def __init__(self, env, task):
        super(DistanceReward, self).__init__(env, task)
        self.prev_obj1_position = None
        self.prev_obj2_position = None

    def decide(self, observation=None):
        return random.randint(0, self.env.num_networks-1)

    def compute(self, observation):
        """
        Compute reward signal based on distance between 2 objects. The position of the objects must be present in observation.

        Params:
            :param observation: (list) Observation of the environment
        Returns:
            :return reward: (float) Reward signal for the environment
        """
        o1 = observation["actual_state"]
        o2 = observation["goal_state"]
        collision = self.env.robot.collision
        reward = self.calc_dist_diff(o1, o2) + collision * (-1)
        #self.task.check_distance_threshold(observation)
        self.task.check_goal()
        self.rewards_history.append(reward)
        return reward

    def reset(self):
        """
        Reset stored value of distance between 2 objects. Call this after the end of an episode.
        """
        self.prev_obj1_position = None
        self.prev_obj2_position = None

    def calc_dist_diff(self, obj1_position, obj2_position):
        """
        Calculate change in the distance between 2 objects in previous and in current step. Normalize the change by the value of distance in previous step.

        Params:
            :param obj1_position: (list) Position of the first object
            :param obj2_position: (list) Position of the second object
        Returns:
            :return norm_diff: (float) Normalized difference of distances between 2 objects in previsous and in current step
        """
        if self.prev_obj1_position is None and self.prev_obj2_position is None:
            self.prev_obj1_position = obj1_position
            self.prev_obj2_position = obj2_position
        self.prev_diff = self.task.calc_distance(self.prev_obj1_position, self.prev_obj2_position)

        current_diff = self.task.calc_distance(obj1_position, obj2_position)
        norm_diff = (self.prev_diff - current_diff) / self.prev_diff

        self.prev_obj1_position = obj1_position
        self.prev_obj2_position = obj2_position

        return norm_diff

class ReachReward(Reward):
    """
    Reward class for Reach task

    Parameters:
        :param env: (object) Environment, where the training takes place
        :param task: (object) Task that is being trained, instance of a class TaskModule
    """
    def __init__(self, env, task):
        super(ReachReward, self).__init__(env, task)
        self.prev_action = None
        self.init_distance = None

    def compute(self, observation, action):
        """
        Compute reward signal based on distance between 2 objects. The position of the objects must be present in observation.

        Params:
            :param observation: (list) Observation of the environment
        Returns:
            :return reward: (float) Reward signal for the environment
        """
        if self.prev_action is None:
            self.prev_action = np.array(action)
        o1 = observation["actual_state"]
        o2 = observation["goal_state"]
        for key in observation["additional_obs"]:
            if key == "endeff_xyz":
                o3 = observation["additional_obs"][key]
            elif key == "endeff_6D":
                o3 = observation["additional_obs"][key][:3]
        a = np.array(action) - self.prev_action
        vec = np.array(o2) - np.array(o3)
        dist = np.linalg.norm(vec)
        if self.init_distance is None:
            self.init_distance = dist
        reward_dist = (-1)*(dist/self.init_distance)
        reward_ctrl = (-0.1)*np.square(a).sum()
        collision = self.env.robot.collision
        reward_coll = (-1)*collision
        finished = self.task.check_distance_threshold(observation)
        if finished:
            reward = 10
            print(f"achieved!!! reward: sum {reward}")
        else:
            reward = reward_dist + reward_ctrl + reward_coll
            print(f"not achieved... reward: dist {reward_dist}, ctrl {reward_ctrl}, coll {reward_coll}, finished {finished}, sum {reward}")
        self.task.check_goal()
        self.rewards_history.append(reward)
        self.prev_action = np.array(action)
        return reward

    def reset(self):
        """
        Reset stored value of distance between 2 objects. Call this after the end of an episode.
        """
        self.prev_action = None
        self.init_distance = None
    
class PnPReward(Reward):
    """
    Pick and place with simple Distance reward. The gripper is operated automatically.
    Applicable for 1 network.

    Parameters:
        :param env: (object) Environment, where the training takes place
        :param task: (object) Task that is being trained, instance of a class TaskModule
    """
    def __init__(self, env, task):
        super(PnPReward, self).__init__(env, task)
        self.prev_action = None
        self.init_distance_1 = None
        self.init_distance_2 = None
    
    def compute(self, observation, action):
        """
        Compute reward signal based on distance between 2 objects. The position of the objects must be present in observation.

        Params:
            :param observation: (list) Observation of the environment
        Returns:
            :return reward: (float) Reward signal for the environment
        """
        if self.prev_action is None:
            self.prev_action = np.array(action)
        o1 = observation["actual_state"][:3]
        if o1[2] < 0.0: # remove error in physics engine
            o1[2] = 0.0
        o2 = observation["goal_state"][:3]
        for key in observation["additional_obs"]:
            if key == "endeff_xyz":
                o3 = observation["additional_obs"][key]
            elif key == "endeff_6D":
                o3 = observation["additional_obs"][key][:3]
        a = np.array(action) - self.prev_action
        vec_1 = np.array(o1) - np.array(o3)
        vec_2 = np.array(o2) - np.array(o3)
        dist_1 = np.linalg.norm(vec_1)
        dist_2 = np.linalg.norm(vec_2)
        reward_ctrl = (-0.1)*np.square(a).sum()
        collision = self.env.robot.collision
        reward_coll = (-1)*collision
        finished = self.env.robot.pnp_finish
        if finished:
            reward = 100
            print(f"achieved!!! reward: sum {reward}")
        elif self.env.robot.gripper_active:
            if self.init_distance_2 is None:
                self.init_distance_2 = dist_2
                reward = 10
                print(f"grasped!!! reward: sum {reward}")
            else:
                reward_dist = (-1)*(dist_2/self.init_distance_2)
                reward = reward_dist + reward_ctrl + reward_coll + 2
                print(f"grasped... reward: dist {reward_dist}, ctrl {reward_ctrl}, coll {reward_coll}, grip {self.env.robot.gripper_active}, finished {finished}, sum {reward}")
        else:
            if self.init_distance_1 is None:
                self.init_distance_1 = dist_1
            reward_dist = (-1)*(dist_1/self.init_distance_1)
            reward = reward_dist + reward_ctrl + reward_coll
            print(f"not grasped... reward: dist {reward_dist}, ctrl {reward_ctrl}, coll {reward_coll}, grip {self.env.robot.gripper_active}, finished {finished}, sum {reward}")
        self.task.check_goal()
        self.rewards_history.append(reward)
        self.prev_action = np.array(action)
        return reward
    
    def reset(self):
        """
        Reset stored value of distance between 2 objects. Call this after the end of an episode.
        """
        self.prev_action = None
        self.init_distance_1 = None
        self.init_distance_2 = None

class PushReward(Reward):
    """
    Reward class for push task

    Parameters:
        :param env: (object) Environment, where the training takes place
        :param task: (object) Task that is being trained, instance of a class TaskModule
    """
    def __init__(self, env, task):
        super(PushReward, self).__init__(env, task)
        self.prev_action = None
        # self.prev_o1 = None
        self.init_distance = None
        self.init_near = None

    def compute(self, observation, action):
        """
        Compute reward signal based on distance between 2 objects. The position of the objects must be present in observation.

        Params:
            :param observation: (list) Observation of the environment
        Returns:
            :return reward: (float) Reward signal for the environment
        """
        if self.prev_action is None:
            self.prev_action = np.array(action)
        o1 = observation["actual_state"]
        if o1[2] < 0.0: # remove error in physics engine
            o1[2] = 0.0
        o2 = observation["goal_state"]
        for key in observation["additional_obs"]:
            if key == "endeff_xyz":
                o3 = observation["additional_obs"][key]
            elif key == "endeff_6D":
                o3 = observation["additional_obs"][key][:3]
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
        collision = self.env.robot.collision
        reward_coll = (-1)*collision
        finished = self.task.check_distance_threshold(observation)
        if finished:
            reward = 100
            print(f"achieved!!! reward: sum {reward}")
        elif near <= 0.05:
            reward = reward_dist + reward_ctrl + reward_coll + reward_near + 2
            print(f"near... reward: dist {reward_dist}, ctrl {reward_ctrl}, coll {reward_coll}, near {reward_near}, finished {finished}, sum {reward}")
        else:
            reward = reward_dist + reward_ctrl + reward_coll + reward_near
            # reward = reward_dist + reward_ctrl + reward_coll + reward_change
            print(f"not achieved... reward: dist {reward_dist}, ctrl {reward_ctrl}, coll {reward_coll}, near {reward_near}, finished {finished}, sum {reward}")
        self.task.check_goal()
        self.rewards_history.append(reward)
        self.prev_action = np.array(action)
        # self.prev_o1 = o1
        return reward

    def reset(self):
        """
        Reset stored value of distance between 2 objects. Call this after the end of an episode.
        """
        self.prev_action = None
        # self.prev_o1 = None
        self.init_distance = None
        self.init_near = None