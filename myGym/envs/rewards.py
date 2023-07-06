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

    def compute(self, observation, action):
        # o2-o3
        o1 = observation["actual_state"]
        o2 = observation["goal_state"]
        o3 = observation["additional_obs"]["endeff_6D"][:3]
        goal_dist = np.linalg.norm(np.array(o2)-np.array(o3))
        reward_reach = 0.2*(1-np.tanh(10*goal_dist))
        reward_success = 13 if goal_dist < 0.05 else 0
        collision = self.env.robot.collision
        reward = max(reward_reach, reward_success) + (-0.1*collision)
        # print(f"reward:{reward_reach, reward_success}")
        self.task.check_goal()
        self.rewards_history.append(reward)
        return reward

    def reset(self):
        """
        Reset stored value of distance between 2 objects. Call this after the end of an episode.
        """
        pass
    
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

    def compute(self, observation, action):
        # o1-o3 -> o2-o3
        o1 = observation["actual_state"]
        o2 = observation["goal_state"]
        o3 = observation["additional_obs"]["endeff_6D"][:3]
        target_dist = np.linalg.norm(np.array(o1)-np.array(o3)) # o1-o2
        goal_dist = np.linalg.norm(np.array(o2)-np.array(o3)) # o2-o3
        reward_reach = 0.2*(1-np.tanh(10*target_dist))
        reward_approach = 0.3+0.4*(1-np.tanh(5*goal_dist)) if self.env.robot.gripper_active else 0
        reward_success = 45 if self.env.robot.pnp_finish else 0
        collision = self.env.robot.collision
        reward = max(reward_reach, reward_approach, reward_success) + (-0.1*collision)
        # print(f"reward:{reward_reach, reward_approach, reward_success}")
        self.task.check_goal()
        self.rewards_history.append(reward)
        return reward
    
    def reset(self):
        """
        Reset stored value of distance between 2 objects. Call this after the end of an episode.
        """
        pass

class PrePushReward(Reward):
    """
    Reward class for push task

    Parameters:
        :param env: (object) Environment, where the training takes place
        :param task: (object) Task that is being trained, instance of a class TaskModule
    """
    def __init__(self, env, task):
        super(PrePushReward, self).__init__(env, task)

    def compute(self, observation, action):
        # o1-o3 -> o1-o2
        o1 = observation["actual_state"]
        o2 = observation["goal_state"]
        o3 = observation["additional_obs"]["endeff_6D"][:3]
        target_dist = np.linalg.norm(np.array(o1)-np.array(o3)) # o1-o2
        goal_dist = np.linalg.norm(np.array(o1)-np.array(o2)) # o1-o3
        reward_reach = 0.2*(1-np.tanh(10*target_dist))
        reward_approach = 0.3+0.4*(1-np.tanh(5*goal_dist)) if target_dist < 0.05 else 0
        reward_success = 45 if goal_dist < 0.05 else 0
        collision = self.env.robot.collision
        reward = max(reward_reach, reward_approach, reward_success) + (-0.1*collision)
        # print(f"reward:{reward_reach, reward_approach, reward_success}")
        self.task.check_goal()
        self.rewards_history.append(reward)
        return reward
    
    def reset(self):
        """
        Reset stored value of distance between 2 objects. Call this after the end of an episode.
        """
        pass

class PushReward(Reward):
    """
    Reward class for push task

    Parameters:
        :param env: (object) Environment, where the training takes place
        :param task: (object) Task that is being trained, instance of a class TaskModule
    """
    def __init__(self, env, task):
        super(PushReward, self).__init__(env, task)
        self.pre_o1 = None

    def compute(self, observation, action):
        # o1-o3 -> o1-o2
        o1 = observation["actual_state"]
        if self.pre_o1 == None:
            self.pre_o1 = o1
        o2 = observation["goal_state"]
        o3 = observation["additional_obs"]["endeff_6D"][:3]
        target_dist = np.linalg.norm(np.array(o1)-np.array(o3)) # o1-o2
        goal_dist = np.linalg.norm(np.array(o1)-np.array(o2)) # o1-o3
        change = 1 if np.linalg.norm(np.array(self.pre_o1) - np.array(o1)) > 0.01 else 0
        reward_reach = 0.2*(1-np.tanh(10*target_dist))
        reward_approach = 0.3+0.4*(1-np.tanh(5*goal_dist)) if target_dist < 0.05 else 0
        reward_success = 45 if goal_dist < 0.05 else 0
        collision = self.env.robot.collision
        reward = max(reward_reach, reward_approach, reward_success) + (-0.1*collision + 1*change)
        # print(f"reward:{reward_reach, reward_approach, reward_success},collision:{collision},change:{change}")
        self.task.check_goal()
        self.rewards_history.append(reward)
        self.pre_o1 = o1
        return reward
    
    def reset(self):
        """
        Reset stored value of distance between 2 objects. Call this after the end of an episode.
        """
        self.pre_o1  = None