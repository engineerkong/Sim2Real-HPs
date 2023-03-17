from __future__ import absolute_import
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple, Union, Type, TypeVar
import torch as th

from .utils import is_image_space, get_device, is_vectorized_observation, obs_as_tensor, maybe_transpose, FlattenExtractor
from .utils import get_action_dim, create_mlp, preprocess_obs

class ContinuousCritic(th.nn.Module):
    u"""
    ContinuousCritic - BaseModel - nn.Module
    """

    def __init__(
        self,
        observation_space,
        action_space,
        net_arch,
        features_extractor,
        features_dim,
        activation_fn = th.nn.ReLU,
        normalize_images = True,
        n_critics = 2,
        share_features_extractor = True,
        features_extractor_class = FlattenExtractor,
        features_extractor_kwargs = None,
        optimizer_class = th.optim.Adam,
        optimizer_kwargs = None,

    ):
        
        super(ContinuousCritic, self).__init__()

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

        action_dim = get_action_dim(self.action_space)

        self.share_features_extractor = share_features_extractor
        self.n_critics = n_critics
        self.q_networks = []
        for idx in range(n_critics):
            q_net = create_mlp(features_dim + action_dim, 1, net_arch, activation_fn)
            q_net = th.nn.Sequential(*q_net)
            self.add_module(u"qf{}".format(idx), q_net)
            self.q_networks.append(q_net)

    def set_training_mode(self, mode):

        self.train(mode)
