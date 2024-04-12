import numpy as np
from math import sqrt

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

class GymReward(Reward):
    """
    Reward class for Gym reward function on Reach Task.

    Parameters:
        :param env: (object) Environment, where the training takes place
        :param task: (object) Task that is being trained, instance of a class TaskModule
    """
    def __init__(self, env, task):
        super(ComposuiteReward, self).__init__(env, task)


    def compute(self, observation, action):
        o1 = observation["actual_state"]
        o2 = observation["goal_state"]
        vec = o1 - o2
        reward_dist = -np.linalg.norm(vec)
        reward_ctrl = -np.square(action).sum()
        reward = reward_dist + reward_ctrl
        self.task.check_goal()
        self.rewards_history.append(reward)
        return reward

    def reset(self):
        """
        Reset stored value of distance between 2 objects. Call this after the end of an episode.
        """
        pass

class MyGymReward(Reward):
    """
    Reward class for MyGym reward function on Reach Task.

    Parameters:
        :param env: (object) Environment, where the training takes place
        :param task: (object) Task that is being trained, instance of a class TaskModule
    """
    def __init__(self, env, task):
        super(MyGymReward, self).__init__(env, task)
        self.prev_obj1_position = None
        self.prev_obj2_position = None

    def compute(self, observation, action):
        """
        Compute reward signal based on distance between 2 objects. The position of the objects must be present in observation.

        Params:
            :param observation: (list) Observation of the environment
        Returns:
            :return reward: (float) Reward signal for the environment
        """
        o1 = observation["actual_state"]
        o2 = observation["goal_state"]
        reward = self.calc_dist_diff(o1, o2)
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

class ComposuiteReward(Reward):
    """
    Reward class for Composuite reward function on Reach Task.

    Parameters:
        :param env: (object) Environment, where the training takes place
        :param task: (object) Task that is being trained, instance of a class TaskModule
    """
    def __init__(self, env, task):
        super(ComposuiteReward, self).__init__(env, task)

    def compute(self, observation, action):
        o1 = observation["actual_state"]
        o2 = observation["goal_state"]
        reward_reach = 0.2*(1-np.tanh(10*self.cal_dist(o1,o2)))
        reward_success = 1 if self.cal_dist(o1,o2) < 0.05 else 0
        reward = max(reward_reach, reward_success)
        # print(f"reward:{reward_reach, reward_success}")
        self.task.check_goal()
        self.rewards_history.append(reward)
        return reward

    def reset(self):
        """
        Reset stored value of distance between 2 objects. Call this after the end of an episode.
        """
        pass

    def cal_dist(self, obj1_position, obj2_position):
        """
        Calculate distance between 2 objects in current step.

        Params:
            :param obj1_position: (list) Position of the first object
            :param obj2_position: (list) Position of the second object
        Returns:
            :return dist: (float) Distances between 2 objects in current step
        """
        dist = np.linalg.norm(np.array(obj1_position)-np.array(obj2_position))

        return dist