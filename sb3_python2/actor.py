from __future__ import absolute_import
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple, Union, Type, TypeVar
import torch as th

from .utils import is_image_space, get_device, is_vectorized_observation, obs_as_tensor, maybe_transpose, FlattenExtractor
from .utils import get_action_dim, create_mlp, preprocess_obs
from .distribution import SquashedDiagGaussianDistribution

LOG_STD_MAX = 2
LOG_STD_MIN = -20

class Actor(th.nn.Module):
    u"""
    Actor - BasePolicy - BaseModel - nn.Module
    """

    def __init__(
        self,
        observation_space,
        action_space,
        net_arch,
        features_extractor,
        features_dim,
        activation_fn = th.nn.ReLU,
        use_sde = False,
        log_std_init = -3,
        full_std = True,
        use_expln = False,
        clip_mean = 2.0,
        normalize_images = True,
        squash_output=True,
        features_extractor_class = FlattenExtractor,
        features_extractor_kwargs = None,
        optimizer_class = th.optim.Adam,
        optimizer_kwargs = None,
    ):

        super(Actor, self).__init__()
        
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

        self.use_sde = use_sde
        self.sde_features_extractor = None
        self.net_arch = net_arch
        self.features_dim = features_dim
        self.activation_fn = activation_fn
        self.log_std_init = log_std_init
        self.use_expln = use_expln
        self.full_std = full_std
        self.clip_mean = clip_mean

        action_dim = get_action_dim(self.action_space)
        latent_pi_net = create_mlp(features_dim, -1, net_arch, activation_fn)
        print(latent_pi_net) # depend on in/out layers
        self.latent_pi = th.nn.Sequential(*latent_pi_net)
        last_layer_dim = net_arch[-1] if len(net_arch) > 0 else features_dim

        if self.use_sde == False:
            self.action_dist = SquashedDiagGaussianDistribution(action_dim)
            self.mu = th.nn.Linear(last_layer_dim, action_dim)
            self.log_std = th.nn.Linear(last_layer_dim, action_dim)

    def get_action_dist_params(self, obs):

        features = self.extract_features(obs, self.features_extractor)
        latent_pi = self.latent_pi(features)
        mean_actions = self.mu(latent_pi)

        if self.use_sde:
            return mean_actions, self.log_std, dict(latent_sde=latent_pi)
        log_std = self.log_std(latent_pi)
        log_std = th.clamp(log_std, LOG_STD_MIN, LOG_STD_MAX)
        return mean_actions, log_std, {}

    def forward(self, obs, deterministic = False):
        mean_actions, log_std, kwargs = self.get_action_dist_params(obs)
        return self.action_dist.actions_from_params(mean_actions, log_std, deterministic=deterministic, **kwargs)

    def _predict(self, observation, deterministic = False):
        return self(observation, deterministic)

    def extract_features(self, obs, features_extractor):

        preprocessed_obs = preprocess_obs(obs, self.observation_space, normalize_images=self.normalize_images)
        return features_extractor(preprocessed_obs)