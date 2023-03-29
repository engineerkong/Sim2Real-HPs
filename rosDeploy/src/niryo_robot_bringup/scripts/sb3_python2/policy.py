from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple, Union, Type, TypeVar
import gym
import torch as th
import numpy as np
import copy

from .utils import is_image_space, get_device, is_vectorized_observation, obs_as_tensor, maybe_transpose, FlattenExtractor, CombinedExtractor
from .actor import Actor
from .critic import ContinuousCritic

class MlpPolicy(th.nn.Module):
    u"""
    MlpPolicy - BasePolicy - BaseModel - nn.Module
    """

    def __init__(
        self,
        observation_space,
        action_space,
        lr_schedule,
        net_arch = None,
        activation_fn = th.nn.ReLU,
        use_sde = False,
        log_std_init = -3,
        use_expln = False,
        clip_mean = 2.0,
        features_extractor_class = FlattenExtractor,
        features_extractor_kwargs = None,
        normalize_images = True,
        optimizer_class = th.optim.Adam,
        optimizer_kwargs = None,
        n_critics = 2,
        share_features_extractor = False,
        squash_output = True,
        features_extractor = None,
    ):
        
        super(MlpPolicy, self).__init__()
        
        if optimizer_kwargs is None:
            optimizer_kwargs = {}

        if features_extractor_kwargs is None:
            features_extractor_kwargs = {}

        self.observation_space = observation_space
        self.action_space = action_space
        self.features_extractor = features_extractor
        self.normalize_images = normalize_images

        self.optimizer_class = optimizer_class
        self.optimizer_kwargs = optimizer_kwargs
        self.optimizer = None

        self.features_extractor_class = features_extractor_class
        self.features_extractor_kwargs = features_extractor_kwargs

        self._squash_output = squash_output
        if net_arch is None:
            net_arch = [256, 256]

        actor_arch, critic_arch = net_arch, net_arch

        self.net_arch = net_arch
        self.activation_fn = activation_fn
        self.net_args = {
            u"observation_space": self.observation_space,
            u"action_space": self.action_space,
            u"net_arch": actor_arch,
            u"activation_fn": self.activation_fn,
            u"normalize_images": normalize_images,
        }
        self.actor_kwargs = self.net_args.copy()

        sde_kwargs = {
            u"use_sde": use_sde,
            u"log_std_init": log_std_init,
            u"use_expln": use_expln,
            u"clip_mean": clip_mean,
        }
        self.actor_kwargs.update(sde_kwargs)
        self.critic_kwargs = self.net_args.copy()
        self.critic_kwargs.update(
            {
                u"n_critics": n_critics,
                u"net_arch": critic_arch,
                u"share_features_extractor": share_features_extractor,
            }
        )

        self.actor, self.actor_target = None, None
        self.critic, self.critic_target = None, None
        self.share_features_extractor = share_features_extractor

        self._build(lr_schedule)

    def _update_features_extractor(
        self,
        net_kwargs,
        features_extractor = None,
    ):

        net_kwargs = net_kwargs.copy()
        if features_extractor is None:
            features_extractor = self.make_features_extractor()
        net_kwargs.update(dict(features_extractor=features_extractor, features_dim=features_extractor.features_dim))
        
        return net_kwargs

    def make_features_extractor(self):

        return self.features_extractor_class(self.observation_space, **self.features_extractor_kwargs)

    @property
    def device(self):

        for param in self.parameters():
            return param.device
        
        return get_device(u"cpu")

    def obs_to_tensor(self, observation):

        vectorized_env = False
        if isinstance(observation, dict):

            observation = copy.deepcopy(observation)
            for key, obs in observation.items():
                obs_space = self.observation_space.spaces[key]
                if is_image_space(obs_space):
                    obs_ = maybe_transpose(obs, obs_space)
                else:
                    obs_ = np.array(obs)
                vectorized_env = vectorized_env or is_vectorized_observation(obs_, obs_space)

                observation[key] = obs_.reshape((-1,) + self.observation_space[key].shape)

        elif is_image_space(self.observation_space):

            observation = maybe_transpose(observation, self.observation_space)

        else:
            observation = np.array(observation)

        if not isinstance(observation, dict):

            vectorized_env = is_vectorized_observation(observation, self.observation_space)

            observation = observation.reshape((-1,) + self.observation_space.shape)

        observation = obs_as_tensor(observation, self.device)

        return observation, vectorized_env

    @property
    def squash_output(self):

        return self._squash_output

    def predict(
        self,
        observation,
        state = None,
        episode_start = None,
        deterministic = False,
    ):

        observation, vectorized_env = self.obs_to_tensor(observation)

        with th.no_grad():
            actions = self._predict(observation, deterministic=deterministic)
        actions = actions.cpu().numpy().reshape((-1,) + self.action_space.shape)

        if isinstance(self.action_space, gym.spaces.Box):
            if self.squash_output:
                actions = self.unscale_action(actions)
            else:
                actions = np.clip(actions, self.action_space.low, self.action_space.high)

        if not vectorized_env:
            actions = actions.squeeze(axis=0)

        return actions, state

    def scale_action(self, action):

        low, high = self.action_space.low, self.action_space.high
        return 2.0 * ((action - low) / (high - low)) - 1.0

    def unscale_action(self, scaled_action):

        low, high = self.action_space.low, self.action_space.high
        return low + (0.5 * (scaled_action + 1.0) * (high - low))

    def _build(self, lr_schedule):
        
        self.actor = self.make_actor()
        self.actor.optimizer = self.optimizer_class(self.actor.parameters(), lr=lr_schedule(1), **self.optimizer_kwargs)

        if self.share_features_extractor:
            self.critic = self.make_critic(features_extractor=self.actor.features_extractor)
            critic_parameters = [param for name, param in self.critic.named_parameters() if u"features_extractor" not in name]
        else:
            self.critic = self.make_critic(features_extractor=None)
            critic_parameters = self.critic.parameters()

        self.critic_target = self.make_critic(features_extractor=None)
        self.critic_target.load_state_dict(self.critic.state_dict())

        self.critic.optimizer = self.optimizer_class(critic_parameters, lr=lr_schedule(1), **self.optimizer_kwargs)

        self.critic_target.set_training_mode(False)

    def make_actor(self, features_extractor = None):

        actor_kwargs = self._update_features_extractor(self.actor_kwargs, features_extractor)

        return Actor(**actor_kwargs)
    
    def make_critic(self, features_extractor = None):
    
        critic_kwargs = self._update_features_extractor(self.critic_kwargs, features_extractor)
        
        return ContinuousCritic(**critic_kwargs)
    
    def _predict(self, observation, deterministic = False):

        return self.actor(observation, deterministic)
    
class MultiInputPolicy(MlpPolicy):
    u"""
    MultiInputPolicy - MlpPolicy - BasePolicy - BaseModel - nn.Module
    """

    def __init__(
        self,
        observation_space,
        action_space,
        lr_schedule,
        net_arch = None,
        activation_fn = th.nn.ReLU,
        use_sde = False,
        log_std_init = -3,
        use_expln = False,
        clip_mean = 2.0,
        features_extractor_class = CombinedExtractor,
        features_extractor_kwargs = None,
        normalize_images = True,
        optimizer_class = th.optim.Adam,
        optimizer_kwargs = None,
        n_critics = 2,
        share_features_extractor = False,
    ):
        super(MultiInputPolicy, self).__init__(
            observation_space,
            action_space,
            lr_schedule,
            net_arch,
            activation_fn,
            use_sde,
            log_std_init,
            use_expln,
            clip_mean,
            features_extractor_class,
            features_extractor_kwargs,
            normalize_images,
            optimizer_class,
            optimizer_kwargs,
            n_critics,
            share_features_extractor,
        )