from __future__ import division
from __future__ import absolute_import
import numpy as np
import warnings
import psutil
from collections import deque
from enum import Enum

from sb3_py2.preprocessing import get_action_dim, get_obs_shape

class BaseBuffer(object):
    u"""
    Base class that represent a buffer (rollout or replay)

    :param buffer_size: Max number of element in the buffer
    :param observation_space: Observation space
    :param action_space: Action space
    :param device: PyTorch device
        to which the values will be converted
    :param n_envs: Number of parallel environments
    """

    def __init__(
        self,
        buffer_size,
        observation_space,
        action_space,
        device = u"cpu",
        n_envs = 1,
    ):
        super(BaseBuffer, self).__init__()
        self.buffer_size = buffer_size
        self.observation_space = observation_space
        self.action_space = action_space
        self.obs_shape = get_obs_shape(observation_space)

        self.action_dim = get_action_dim(action_space)
        self.pos = 0
        self.full = False
        self.device = device
        self.n_envs = n_envs

    def reset(self):
        u"""
        Reset the buffer.
        """
        self.pos = 0
        self.full = False

    
class RolloutBuffer(BaseBuffer):
    u"""
    Rollout buffer used in on-policy algorithms like A2C/PPO.
    It corresponds to ``buffer_size`` transitions collected
    using the current policy.
    This experience will be discarded after the policy update.
    In order to use PPO objective, we also store the current value of each state
    and the log probability of each taken action.

    The term rollout here refers to the model-free notion and should not
    be used with the concept of rollout used in model-based RL or planning.
    Hence, it is only involved in policy and value function training but not action selection.

    :param buffer_size: Max number of element in the buffer
    :param observation_space: Observation space
    :param action_space: Action space
    :param device:
    :param gae_lambda: Factor for trade-off of bias vs variance for Generalized Advantage Estimator
        Equivalent to classic advantage when set to 1.
    :param gamma: Discount factor
    :param n_envs: Number of parallel environments
    """

    def __init__(
        self,
        buffer_size,
        observation_space,
        action_space,
        device = u"cpu",
        gae_lambda = 1,
        gamma = 0.99,
        n_envs = 1,
    ):

        super(RolloutBuffer, self).__init__(buffer_size, observation_space, action_space, device, n_envs=n_envs)
        self.gae_lambda = gae_lambda
        self.gamma = gamma
        self.observations, self.actions, self.rewards, self.advantages = None, None, None, None
        self.returns, self.episode_starts, self.values, self.log_probs = None, None, None, None
        self.generator_ready = False
        self.reset()

    def reset(self):

        self.observations = np.zeros((self.buffer_size, self.n_envs) + self.obs_shape, dtype=np.float32)
        self.actions = np.zeros((self.buffer_size, self.n_envs, self.action_dim), dtype=np.float32)
        self.rewards = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.returns = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.episode_starts = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.values = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.log_probs = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.advantages = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.generator_ready = False
        super(RolloutBuffer, self).reset()
    
class DictRolloutBuffer(RolloutBuffer):
    u"""
    Dict Rollout buffer used in on-policy algorithms like A2C/PPO.
    Extends the RolloutBuffer to use dictionary observations

    It corresponds to ``buffer_size`` transitions collected
    using the current policy.
    This experience will be discarded after the policy update.
    In order to use PPO objective, we also store the current value of each state
    and the log probability of each taken action.

    The term rollout here refers to the model-free notion and should not
    be used with the concept of rollout used in model-based RL or planning.
    Hence, it is only involved in policy and value function training but not action selection.

    :param buffer_size: Max number of element in the buffer
    :param observation_space: Observation space
    :param action_space: Action space
    :param device:
    :param gae_lambda: Factor for trade-off of bias vs variance for Generalized Advantage Estimator
        Equivalent to classic advantage when set to 1.
    :param gamma: Discount factor
    :param n_envs: Number of parallel environments
    """

    def __init__(
        self,
        buffer_size,
        observation_space,
        action_space,
        device = u"cpu",
        gae_lambda = 1,
        gamma = 0.99,
        n_envs = 1,
    ):

        super(RolloutBuffer, self).__init__(buffer_size, observation_space, action_space, device, n_envs=n_envs)

        assert isinstance(self.obs_shape, dict), u"DictRolloutBuffer must be used with Dict obs space only"

        self.gae_lambda = gae_lambda
        self.gamma = gamma
        self.observations, self.actions, self.rewards, self.advantages = None, None, None, None
        self.returns, self.episode_starts, self.values, self.log_probs = None, None, None, None
        self.generator_ready = False
        self.reset()

    def reset(self):
        assert isinstance(self.obs_shape, dict), u"DictRolloutBuffer must be used with Dict obs space only"
        self.observations = {}
        for key, obs_input_shape in self.obs_shape.items():
            self.observations[key] = np.zeros((self.buffer_size, self.n_envs) + obs_input_shape, dtype=np.float32)
        self.actions = np.zeros((self.buffer_size, self.n_envs, self.action_dim), dtype=np.float32)
        self.rewards = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.returns = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.episode_starts = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.values = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.log_probs = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.advantages = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.generator_ready = False
        super(RolloutBuffer, self).reset()

class ReplayBuffer(BaseBuffer):
    u"""
    Replay buffer used in off-policy algorithms like SAC/TD3.

    :param buffer_size: Max number of element in the buffer
    :param observation_space: Observation space
    :param action_space: Action space
    :param device:
    :param n_envs: Number of parallel environments
    :param optimize_memory_usage: Enable a memory efficient variant
        of the replay buffer which reduces by almost a factor two the memory used,
        at a cost of more complexity.
        See https://github.com/DLR-RM/stable-baselines3/issues/37#issuecomment-637501195
        and https://github.com/DLR-RM/stable-baselines3/pull/28#issuecomment-637559274
    :param handle_timeout_termination: Handle timeout termination (due to timelimit)
        separately and treat the task as infinite horizon task.
        https://github.com/DLR-RM/stable-baselines3/issues/284
    """

    def __init__(
        self,
        buffer_size,
        observation_space,
        action_space,
        device = u"cpu",
        n_envs = 1,
        optimize_memory_usage = False,
        handle_timeout_termination = True,
    ):
        super(ReplayBuffer, self).__init__(buffer_size, observation_space, action_space, device, n_envs=n_envs)

        assert n_envs == 1, u"Replay buffer only support single environment for now"

        # Check that the replay buffer can fit into the memory
        if psutil is not None:
            mem_available = psutil.virtual_memory().available

        self.optimize_memory_usage = optimize_memory_usage

        self.observations = np.zeros((self.buffer_size, self.n_envs) + self.obs_shape, dtype=observation_space.dtype)

        if optimize_memory_usage:
            # `observations` contains also the next observation
            self.next_observations = None
        else:
            self.next_observations = np.zeros((self.buffer_size, self.n_envs) + self.obs_shape, dtype=observation_space.dtype)

        self.actions = np.zeros((self.buffer_size, self.n_envs, self.action_dim), dtype=action_space.dtype)

        self.rewards = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.dones = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        # Handle timeouts termination properly if needed
        # see https://github.com/DLR-RM/stable-baselines3/issues/284
        self.handle_timeout_termination = handle_timeout_termination
        self.timeouts = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)

        if psutil is not None:
            total_memory_usage = self.observations.nbytes + self.actions.nbytes + self.rewards.nbytes + self.dones.nbytes

            if self.next_observations is not None:
                total_memory_usage += self.next_observations.nbytes

            if total_memory_usage > mem_available:
                # Convert to GB
                total_memory_usage /= 1e9
                mem_available /= 1e9
                warnings.warn("warning")

class DictReplayBuffer(ReplayBuffer):
    u"""
    Dict Replay buffer used in off-policy algorithms like SAC/TD3.
    Extends the ReplayBuffer to use dictionary observations

    :param buffer_size: Max number of element in the buffer
    :param observation_space: Observation space
    :param action_space: Action space
    :param device:
    :param n_envs: Number of parallel environments
    :param optimize_memory_usage: Enable a memory efficient variant
        Disabled for now (see https://github.com/DLR-RM/stable-baselines3/pull/243#discussion_r531535702)
    :param handle_timeout_termination: Handle timeout termination (due to timelimit)
        separately and treat the task as infinite horizon task.
        https://github.com/DLR-RM/stable-baselines3/issues/284
    """

    def __init__(
        self,
        buffer_size,
        observation_space,
        action_space,
        device = u"cpu",
        n_envs = 1,
        optimize_memory_usage = False,
        handle_timeout_termination = True,
    ):
        super(ReplayBuffer, self).__init__(buffer_size, observation_space, action_space, device, n_envs=n_envs)

        assert isinstance(self.obs_shape, dict), u"DictReplayBuffer must be used with Dict obs space only"
        assert n_envs == 1, u"Replay buffer only support single environment for now"

        # Check that the replay buffer can fit into the memory
        if psutil is not None:
            mem_available = psutil.virtual_memory().available

        assert optimize_memory_usage is False, u"DictReplayBuffer does not support optimize_memory_usage"
        # disabling as this adds quite a bit of complexity
        # https://github.com/DLR-RM/stable-baselines3/pull/243#discussion_r531535702
        self.optimize_memory_usage = optimize_memory_usage

        self.observations = dict((
            key, np.zeros((self.buffer_size, self.n_envs) + _obs_shape, dtype=observation_space[key].dtype))
            for key, _obs_shape in self.obs_shape.items())
        self.next_observations = dict((
            key, np.zeros((self.buffer_size, self.n_envs) + _obs_shape, dtype=observation_space[key].dtype))
            for key, _obs_shape in self.obs_shape.items())

        # only 1 env is supported
        self.actions = np.zeros((self.buffer_size, self.action_dim), dtype=action_space.dtype)
        self.rewards = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)
        self.dones = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)

        # Handle timeouts termination properly if needed
        # see https://github.com/DLR-RM/stable-baselines3/issues/284
        self.handle_timeout_termination = handle_timeout_termination
        self.timeouts = np.zeros((self.buffer_size, self.n_envs), dtype=np.float32)

        if psutil is not None:
            obs_nbytes = 0
            for _, obs in self.observations.items():
                obs_nbytes += obs.nbytes

            total_memory_usage = obs_nbytes + self.actions.nbytes + self.rewards.nbytes + self.dones.nbytes
            if self.next_observations is not None:
                next_obs_nbytes = 0
                for _, obs in self.observations.items():
                    next_obs_nbytes += obs.nbytes
                total_memory_usage += next_obs_nbytes

            if total_memory_usage > mem_available:
                # Convert to GB
                total_memory_usage /= 1e9
                mem_available /= 1e9
                warnings.warn("warning")

class GoalSelectionStrategy(Enum):
    u"""
    The strategies for selecting new goals when
    creating artificial transitions.
    """

    # Select a goal that was achieved
    # after the current step, in the same episode
    FUTURE = 0
    # Select the goal that was achieved
    # at the end of the episode
    FINAL = 1
    # Select a goal that was achieved in the episode
    EPISODE = 2

# For convenience
# that way, we can use string to select a strategy
KEY_TO_GOAL_STRATEGY = {
    u"future": GoalSelectionStrategy.FUTURE,
    u"final": GoalSelectionStrategy.FINAL,
    u"episode": GoalSelectionStrategy.EPISODE,
}

def get_time_limit(env, current_max_episode_length):
    u"""
    Get time limit from environment.

    :param env: Environment from which we want to get the time limit.
    :param current_max_episode_length: Current value for max_episode_length.
    :return: max episode length
    """
    # try to get the attribute from environment
    if current_max_episode_length is None:
        try:
            current_max_episode_length = env.get_attr(u"spec")[0].max_episode_steps
            # Raise the error because the attribute is present but is None
            if current_max_episode_length is None:
                raise AttributeError
        # if not available check if a valid value was passed as an argument
        except AttributeError:
            raise ValueError(
                u"The max episode length could not be inferred.\n"
                u"You must specify a `max_episode_steps` when registering the environment,\n"
                u"use a `gym.wrappers.TimeLimit` wrapper "
                u"or pass `max_episode_length` to the model constructor"
            )
    return current_max_episode_length


class HerReplayBuffer(DictReplayBuffer):
    u"""
    Hindsight Experience Replay (HER) buffer.
    Paper: https://arxiv.org/abs/1707.01495

    .. warning::

      For performance reasons, the maximum number of steps per episodes must be specified.
      In most cases, it will be inferred if you specify ``max_episode_steps`` when registering the environment
      or if you use a ``gym.wrappers.TimeLimit`` (and ``env.spec`` is not None).
      Otherwise, you can directly pass ``max_episode_length`` to the replay buffer constructor.


    Replay buffer for sampling HER (Hindsight Experience Replay) transitions.
    In the online sampling case, these new transitions will not be saved in the replay buffer
    and will only be created at sampling time.

    :param env: The training environment
    :param buffer_size: The size of the buffer measured in transitions.
    :param max_episode_length: The maximum length of an episode. If not specified,
        it will be automatically inferred if the environment uses a ``gym.wrappers.TimeLimit`` wrapper.
    :param goal_selection_strategy: Strategy for sampling goals for replay.
        One of ['episode', 'final', 'future']
    :param device: PyTorch device
    :param n_sampled_goal: Number of virtual transitions to create per real transition,
        by sampling new goals.
    :param handle_timeout_termination: Handle timeout termination (due to timelimit)
        separately and treat the task as infinite horizon task.
        https://github.com/DLR-RM/stable-baselines3/issues/284
    """

    def __init__(
        self,
        env,
        buffer_size,
        device = u"cpu",
        replay_buffer = None,
        max_episode_length = None,
        n_sampled_goal = 4,
        goal_selection_strategy = u"future",
        online_sampling = True,
        handle_timeout_termination = True,
    ):

        super(HerReplayBuffer, self).__init__(buffer_size, env.observation_space, env.action_space, device, env.num_envs)

        # convert goal_selection_strategy into GoalSelectionStrategy if string
        if isinstance(goal_selection_strategy, unicode):
            self.goal_selection_strategy = KEY_TO_GOAL_STRATEGY[goal_selection_strategy.lower()]
        else:
            self.goal_selection_strategy = goal_selection_strategy

        # check if goal_selection_strategy is valid
        assert isinstance(
            self.goal_selection_strategy, GoalSelectionStrategy
        ), "Invalid goal selection strategy, please use one of list"

        self.n_sampled_goal = n_sampled_goal
        # if we sample her transitions online use custom replay buffer
        self.online_sampling = online_sampling
        # compute ratio between HER replays and regular replays in percent for online HER sampling
        self.her_ratio = 1 - (1.0 / (self.n_sampled_goal + 1))
        # maximum steps in episode
        self.max_episode_length = get_time_limit(env, max_episode_length)
        # storage for transitions of current episode for offline sampling
        # for online sampling, it replaces the "classic" replay buffer completely
        her_buffer_size = buffer_size if online_sampling else self.max_episode_length

        self.env = env
        self.buffer_size = her_buffer_size

        if online_sampling:
            replay_buffer = None
        self.replay_buffer = replay_buffer
        self.online_sampling = online_sampling

        # Handle timeouts termination properly if needed
        # see https://github.com/DLR-RM/stable-baselines3/issues/284
        self.handle_timeout_termination = handle_timeout_termination

        # buffer with episodes
        # number of episodes which can be stored until buffer size is reached
        self.max_episode_stored = self.buffer_size // self.max_episode_length
        self.current_idx = 0
        # Counter to prevent overflow
        self.episode_steps = 0

        # Get shape of observation and goal (usually the same)
        self.obs_shape = get_obs_shape(self.env.observation_space.spaces[u"observation"])
        self.goal_shape = get_obs_shape(self.env.observation_space.spaces[u"achieved_goal"])

        # input dimensions for buffer initialization
        input_shape = {
            u"observation": (self.env.num_envs,) + self.obs_shape,
            u"achieved_goal": (self.env.num_envs,) + self.goal_shape,
            u"desired_goal": (self.env.num_envs,) + self.goal_shape,
            u"action": (self.action_dim,),
            u"reward": (1,),
            u"next_obs": (self.env.num_envs,) + self.obs_shape,
            u"next_achieved_goal": (self.env.num_envs,) + self.goal_shape,
            u"next_desired_goal": (self.env.num_envs,) + self.goal_shape,
            u"done": (1,),
        }
        self._observation_keys = [u"observation", u"achieved_goal", u"desired_goal"]
        self._buffer = dict((
                key, np.zeros((self.max_episode_stored, self.max_episode_length) + dim, dtype=np.float32))
            for key, dim in input_shape.items())
        # Store info dicts are it can be used to compute the reward (e.g. continuity cost)
        self.info_buffer = [deque(maxlen=self.max_episode_length) for _ in xrange(self.max_episode_stored)]
        # episode length storage, needed for episodes which has less steps than the maximum length
        self.episode_lengths = np.zeros(self.max_episode_stored, dtype=np.int64)