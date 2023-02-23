from __future__ import absolute_import
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple, Union, Type, TypeVar
import torch as th
from torch.distributions import Bernoulli, Categorical, Normal

from .utils import sum_independent_dims
    
class SquashedDiagGaussianDistribution(object):
    u"""
    SquashedDiagGaussianDistribution - DiagGaussianDistribution - Distribution
    """

    def __init__(self, action_dim, epsilon = 1e-6):

        self.distribution = None
        self.action_dim = action_dim
        self.mean_actions = None
        self.log_std = None
        self.epsilon = epsilon
        self.gaussian_actions = None

    def get_actions(self, deterministic = False):

        if deterministic:
            return self.mode()
        return self.sample()
    
    def proba_distribution(self, mean_actions, log_std):

        action_std = th.ones_like(mean_actions) * log_std.exp()
        self.distribution = Normal(mean_actions, action_std)
        return self

    def actions_from_params(self, mean_actions, log_std, deterministic = False):

        self.proba_distribution(mean_actions, log_std)
        return self.get_actions(deterministic=deterministic)

    def sample(self):

        self.gaussian_actions = self.distribution.rsample()
        return th.tanh(self.gaussian_actions)

    def mode(self):

        self.gaussian_actions = self.distribution.mean
        return th.tanh(self.gaussian_actions)