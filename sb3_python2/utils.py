from __future__ import division
from __future__ import absolute_import
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple, Union, Type, TypeVar
import gym
import torch as th
import numpy as np
import warnings

def get_flattened_obs_dim(observation_space):

    if isinstance(observation_space, gym.spaces.MultiDiscrete):
        return sum(observation_space.nvec)
    else:
        return gym.spaces.utils.flatdim(observation_space)
    
def get_action_dim(action_space):

    if isinstance(action_space, gym.spaces.Box):
        return int(np.prod(action_space.shape))
    elif isinstance(action_space, gym.spaces.Discrete):
        return 1
    elif isinstance(action_space, gym.spaces.MultiDiscrete):
        return int(len(action_space.nvec))
    elif isinstance(action_space, gym.spaces.MultiBinary):
        return int(action_space.n)
    else:
        raise NotImplementedError("{} action space is not supported".format(action_space))
    
def create_mlp(
    input_dim,
    output_dim,
    net_arch,
    activation_fn = th.nn.ReLU,
    squash_output = False,
    with_bias = True,
):

    if len(net_arch) > 0:
        modules = [th.nn.Linear(input_dim, net_arch[0], bias=with_bias), activation_fn()]
    else:
        modules = []

    for idx in range(len(net_arch) - 1): # xrange
        modules.append(th.nn.Linear(net_arch[idx], net_arch[idx + 1], bias=with_bias))
        modules.append(activation_fn())

    if output_dim > 0:
        last_layer_dim = net_arch[-1] if len(net_arch) > 0 else input_dim
        modules.append(th.nn.Linear(last_layer_dim, output_dim, bias=with_bias))
    if squash_output:
        modules.append(th.nn.Tanh())
    
    return modules

def preprocess_obs(
    obs,
    observation_space,
    normalize_images = True,
):

    if isinstance(observation_space, gym.spaces.Box):
        if normalize_images and is_image_space(observation_space):
            return obs.float() / 255.0
        return obs.float()

    elif isinstance(observation_space, gym.spaces.Discrete):
        return th.nn.functional.one_hot(obs.long(), num_classes=observation_space.n).float()

    elif isinstance(observation_space, gym.spaces.MultiDiscrete):
        return th.cat(
            [
                th.nn.functional.one_hot(obs_.long(), num_classes=int(observation_space.nvec[idx])).float()
                for idx, obs_ in enumerate(th.split(obs.long(), 1, dim=1))
            ],
            dim=-1,
        ).view(obs.shape[0], sum(observation_space.nvec))

    elif isinstance(observation_space, gym.spaces.MultiBinary):
        return obs.float()

    elif isinstance(observation_space, gym.spaces.Dict):
        assert isinstance(obs, Dict), "Expected dict, got {}".format(type(obs))
        preprocessed_obs = {}
        for key, _obs in obs.items():
            preprocessed_obs[key] = preprocess_obs(_obs, observation_space[key], normalize_images=normalize_images)
        return preprocessed_obs

    else:
        raise NotImplementedError("Preprocessing not implemented for {}".format(observation_space))
    
def is_image_space_channels_first(observation_space):

    smallest_dimension = np.argmin(observation_space.shape).item()
    if smallest_dimension == 1:
        warnings.warn(u"Treating image space as channels-last, while second dimension was smallest of the three.")
    return smallest_dimension == 0


def is_image_space(
    observation_space,
    check_channels = False,
    normalized_image = False,
):

    check_dtype = check_bounds = not normalized_image
    if isinstance(observation_space, gym.spaces.Box) and len(observation_space.shape) == 3:
        if check_dtype and observation_space.dtype != np.uint8:
            return False

        incorrect_bounds = np.any(observation_space.low != 0) or np.any(observation_space.high != 255)
        if check_bounds and incorrect_bounds:
            return False

        if not check_channels:
            return True
        if is_image_space_channels_first(observation_space):
            n_channels = observation_space.shape[0]
        else:
            n_channels = observation_space.shape[-1]
        return n_channels in [1, 3, 4]
    
    return False

def get_device(device = u"auto"):

    if device == u"auto":
        device = u"cuda"

    device = th.device(device)

    if device.type == th.device(u"cuda").type and not th.cuda.is_available():
        return th.device(u"cpu")

    return device

def is_vectorized_observation(observation, observation_space):

    is_vec_obs_func_dict = {
        gym.spaces.Box: is_vectorized_box_observation,
        gym.spaces.Discrete: is_vectorized_discrete_observation,
        gym.spaces.MultiDiscrete: is_vectorized_multidiscrete_observation,
        gym.spaces.MultiBinary: is_vectorized_multibinary_observation,
        gym.spaces.Dict: is_vectorized_dict_observation,
    }

    for space_type, is_vec_obs_func in is_vec_obs_func_dict.items():
        if isinstance(observation_space, space_type):
            return is_vec_obs_func(observation, observation_space)
    else:
        raise ValueError(u"Error")
    
def is_vectorized_box_observation(observation, observation_space):

    if observation.shape == observation_space.shape:
        return False
    elif observation.shape[1:] == observation_space.shape:
        return True
    else:
        raise ValueError(u"is not vectorized box observation")


def is_vectorized_discrete_observation(observation, observation_space):

    if isinstance(observation, int) or observation.shape == ():
        return False
    elif len(observation.shape) == 1:
        return True
    else:
        raise ValueError(u"is not vectorized discrete observation")


def is_vectorized_multidiscrete_observation(observation, observation_space):

    if observation.shape == (len(observation_space.nvec),):
        return False
    elif len(observation.shape) == 2 and observation.shape[1] == len(observation_space.nvec):
        return True
    else:
        raise ValueError(u"is not vectorized multidiscrete observation")


def is_vectorized_multibinary_observation(observation, observation_space):

    if observation.shape == observation_space.shape:
        return False
    elif len(observation.shape) == len(observation_space.shape) + 1 and observation.shape[1:] == observation_space.shape:
        return True
    else:
        raise ValueError(u"is not vectorized multibinary observation")


def is_vectorized_dict_observation(observation, observation_space):

    all_non_vectorized = True
    for key, subspace in observation_space.spaces.items():
        if observation[key].shape != subspace.shape:
            all_non_vectorized = False
            break

    if all_non_vectorized:
        return False

    all_vectorized = True
    for key, subspace in observation_space.spaces.items():
        if observation[key].shape[1:] != subspace.shape:
            all_vectorized = False
            break

    if all_vectorized:
        return True
    else:
        error_msg = u""
        try:
            is_vectorized_observation(observation[key], observation_space.spaces[key])
        except ValueError as e:
            error_msg = "{}".format(e)
        raise ValueError(u"is not vectorized dict observation")

def obs_as_tensor(obs, device):

    if isinstance(obs, np.ndarray):
        return th.as_tensor(obs, device=device)
    elif isinstance(obs, dict):
        return dict((key, th.as_tensor(_obs, device=device)) for (key, _obs) in obs.items())
    else:
        raise Exception("Unrecognized type of observation {}".format(type(obs)))
    
def maybe_transpose(observation, observation_space):

    if is_image_space(observation_space):
        if not (observation.shape == observation_space.shape or observation.shape[1:] == observation_space.shape):
            transpose_obs = transpose_image(observation)
            if transpose_obs.shape == observation_space.shape or transpose_obs.shape[1:] == observation_space.shape:
                observation = transpose_obs
    return observation

def transpose_image(image):

    if len(image.shape) == 3:
        return np.transpose(image, (2, 0, 1))
    return np.transpose(image, (0, 3, 1, 2))
    
def sum_independent_dims(tensor):

    if len(tensor.shape) > 1:
        tensor = tensor.sum(dim=1)
    else:
        tensor = tensor.sum()
    return tensor

class BaseFeaturesExtractor(th.nn.Module):

    def __init__(self, observation_space, features_dim = 0):
        super(BaseFeaturesExtractor, self).__init__()
        assert features_dim > 0
        self._observation_space = observation_space
        self._features_dim = features_dim

    @property
    def features_dim(self):
        return self._features_dim
    

class FlattenExtractor(BaseFeaturesExtractor):

    def __init__(self, observation_space):
        super(FlattenExtractor, self).__init__(observation_space, get_flattened_obs_dim(observation_space))
        self.flatten = th.nn.Flatten()

    def forward(self, observations):
        return self.flatten(observations)