import gym
import torch as th
import numpy as np
import random

def get_device(device = "auto"):
    """
    Retrieve PyTorch device.
    It checks that the requested device is available first.
    For now, it supports only cpu and cuda.
    By default, it tries to use the gpu.
s
    :param device: One for 'auto', 'cuda', 'cpu'
    :return:
    """
    # Cuda by default
    if device == "auto":
        device = "cuda"
    # Force conversion to th.device
    device = th.device(device)

    # Cuda not available
    if device.type == th.device("cuda").type and not th.cuda.is_available():
        return th.device("cpu")

    return device

def is_vectorized_box_observation(observation, observation_space):
    """
    For box observation type, detects and validates the shape,
    then returns whether or not the observation is vectorized.

    :param observation: the input observation to validate
    :param observation_space: the observation space
    :return: whether the given observation is vectorized or not
    """
    if observation.shape == observation_space.shape:
        return False
    elif observation.shape[1:] == observation_space.shape:
        return True
    else:
        raise ValueError("warning")


def is_vectorized_discrete_observation(observation, observation_space):
    """
    For discrete observation type, detects and validates the shape,
    then returns whether or not the observation is vectorized.

    :param observation: the input observation to validate
    :param observation_space: the observation space
    :return: whether the given observation is vectorized or not
    """
    if observation.shape == ():  # A numpy array of a number, has shape empty tuple '()'
        return False
    elif len(observation.shape) == 1:
        return True
    else:
        raise ValueError("warning")


def is_vectorized_multidiscrete_observation(observation, observation_space):
    """
    For multidiscrete observation type, detects and validates the shape,
    then returns whether or not the observation is vectorized.

    :param observation: the input observation to validate
    :param observation_space: the observation space
    :return: whether the given observation is vectorized or not
    """
    if observation.shape == (len(observation_space.nvec),):
        return False
    elif len(observation.shape) == 2 and observation.shape[1] == len(observation_space.nvec):
        return True
    else:
        raise ValueError("warning")


def is_vectorized_multibinary_observation(observation, observation_space):
    """
    For multibinary observation type, detects and validates the shape,
    then returns whether or not the observation is vectorized.

    :param observation: the input observation to validate
    :param observation_space: the observation space
    :return: whether the given observation is vectorized or not
    """
    if observation.shape == (observation_space.n,):
        return False
    elif len(observation.shape) == 2 and observation.shape[1] == observation_space.n:
        return True
    else:
        raise ValueError("warning")


def is_vectorized_dict_observation(observation, observation_space):
    """
    For dict observation type, detects and validates the shape,
    then returns whether or not the observation is vectorized.

    :param observation: the input observation to validate
    :param observation_space: the observation space
    :return: whether the given observation is vectorized or not
    """
    for key, subspace in observation_space.spaces.items():
        if observation[key].shape == subspace.shape:
            return False

    all_good = True

    for key, subspace in observation_space.spaces.items():
        if observation[key].shape[1:] != subspace.shape:
            all_good = False
            break

    if all_good:
        return True
    else:
        raise ValueError("warning")
    
def is_vectorized_observation(observation, observation_space):
    """
    For every observation type, detects and validates the shape,
    then returns whether or not the observation is vectorized.

    :param observation: the input observation to validate
    :param observation_space: the observation space
    :return: whether the given observation is vectorized or not
    """

    is_vec_obs_func_dict = {
        gym.spaces.Box: is_vectorized_box_observation,
        gym.spaces.Discrete: is_vectorized_discrete_observation,
        gym.spaces.MultiDiscrete: is_vectorized_multidiscrete_observation,
        gym.spaces.MultiBinary: is_vectorized_multibinary_observation,
        gym.spaces.Dict: is_vectorized_dict_observation,
    }

    try:
        is_vec_obs_func = is_vec_obs_func_dict[type(observation_space)]
        return is_vec_obs_func(observation, observation_space)
    except KeyError:
        raise ValueError("warning")
    
def obs_as_tensor(obs, device):
    """
    Moves the observation to the given device.

    :param obs:
    :param device: PyTorch device
    :return: PyTorch tensor of the observation on a desired device.
    """
    if isinstance(obs, np.ndarray):
        return th.as_tensor(obs).to(device)
    elif isinstance(obs, dict):
        return {key: th.as_tensor(_obs).to(device) for (key, _obs) in obs.items()}
    else:
        raise Exception("warning")

def constant_fn(val):
    """
    Create a function that returns a constant
    It is useful for learning rate schedule (to avoid code duplication)

    :param val:
    :return:
    """

    def func(_):
        return val

    return func
    
def get_schedule_fn(value_schedule):
    """
    Transform (if needed) learning rate and clip range (for PPO)
    to callable.

    :param value_schedule:
    :return:
    """
    # If the passed schedule is a float
    # create a constant function
    if isinstance(value_schedule, (float, int)):
        # Cast to float to avoid errors
        value_schedule = constant_fn(float(value_schedule))
    else:
        assert callable(value_schedule)
    return value_schedule

def set_random_seed(seed, using_cuda = False):
    """
    Seed the different random generators.

    :param seed:
    :param using_cuda:
    """
    # Seed python RNG
    random.seed(seed)
    # Seed numpy RNG
    np.random.seed(seed)
    # seed the RNG for all devices (both CPU and CUDA)
    th.manual_seed(seed)

    if using_cuda:
        # Deterministic operations for CuDNN, it may impact performances
        th.backends.cudnn.deterministic = True
        th.backends.cudnn.benchmark = False