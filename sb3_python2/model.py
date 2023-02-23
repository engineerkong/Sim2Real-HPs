from __future__ import absolute_import
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple, Union, Type, TypeVar
import gym
import torch as th

class Model(object):
    u"""
    SAC - OffPolicyAlgorithm - BaseAlgorithm
    """

    Schedule = Callable[[float], float]
    
    def __init__(self, policy_class):

        env = gym.make(u"Pendulum-v0")
        self.obs_space = env.observation_space
        self.act_space = env.action_space
        self.log_ent_coef = th.tensor([0.], requires_grad=True)
        self.lr_schedule = self.get_schedule_fn(0.0003)
        self.policy_class = policy_class

        self.policy = self.policy_class(
            observation_space = self.obs_space,
            action_space = self.act_space,
            lr_schedule = self.lr_schedule
        )
        self.actor = self.policy.actor
        self.critic = self.policy.critic
        self.ent_coef_optimizer = th.optim.Adam([self.log_ent_coef], lr=self.lr_schedule(1))

    def get_schedule_fn(self, value_schedule=Union[Schedule, float, int]):

        if isinstance(value_schedule, (float, int)):
            value_schedule = self.constant_fn(float(value_schedule))
        else:
            assert callable(value_schedule)
        
        return value_schedule

    def constant_fn(self, val):
        
        def func(_):
            return val

        return func

    def predict(self, observation):

        return self.policy.predict(observation)