from typing import Any, Dict, Optional, Tuple, Type, Union

import time
from copy import deepcopy

import gym
import numpy as np
import torch as th
from stable_baselines3.common.buffers import ReplayBuffer
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.noise import ActionNoise
from stable_baselines3.common.type_aliases import GymEnv, GymStepReturn, Schedule
from stable_baselines3.common.vec_env.base_vec_env import VecEnvStepReturn
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3.sac.policies import SACPolicy
from stable_baselines3.sac.sac import SAC

def sac_init(
    self,
    policy: Union[str, Type[SACPolicy]],
    env: Union[GymEnv, str],
    learning_rate: Union[float, Schedule] = 3e-4,
    buffer_size: int = 1_000_000,  # 1e6
    learning_starts: int = 100,
    batch_size: int = 256,
    tau: float = 0.005,
    gamma: float = 0.99,
    train_freq: Union[int, Tuple[int, str]] = 1,
    gradient_steps: int = 1,
    action_noise: Optional[ActionNoise] = None,
    replay_buffer_class: Optional[Type[ReplayBuffer]] = None,
    replay_buffer_kwargs: Optional[Dict[str, Any]] = None,
    optimize_memory_usage: bool = False,
    ent_coef: Union[str, float] = "auto",
    target_update_interval: int = 1,
    target_entropy: Union[str, float] = "auto",
    use_sde: bool = False,
    sde_sample_freq: int = -1,
    use_sde_at_warmup: bool = False,
    tensorboard_log: Optional[str] = None,
    policy_kwargs: Optional[Dict[str, Any]] = None,
    verbose: int = 0,
    seed: Optional[int] = None,
    device: Union[th.device, str] = "auto",
    _init_setup_model: bool = True,
):
    """
    To suit the action space in the environment (Robogym), modify the
    supported_action_spaces in SAC.__init__() to gym.spaces.Space.
    """
    super(SAC, self).__init__(
        policy,
        env,
        learning_rate,
        buffer_size,
        learning_starts,
        batch_size,
        tau,
        gamma,
        train_freq,
        gradient_steps,
        action_noise,
        replay_buffer_class=replay_buffer_class,
        replay_buffer_kwargs=replay_buffer_kwargs,
        policy_kwargs=policy_kwargs,
        tensorboard_log=tensorboard_log,
        verbose=verbose,
        device=device,
        seed=seed,
        use_sde=use_sde,
        sde_sample_freq=sde_sample_freq,
        use_sde_at_warmup=use_sde_at_warmup,
        optimize_memory_usage=optimize_memory_usage,
        supported_action_spaces=(gym.spaces.Space),
        support_multi_env=True,
    )

    self.target_entropy = target_entropy
    self.log_ent_coef = None
    self.ent_coef = ent_coef
    self.target_update_interval = target_update_interval
    self.ent_coef_optimizer = None

    if _init_setup_model:
        self._setup_model()


def dummy_step_wait(self) -> VecEnvStepReturn:
    """
    To deal with the errors:
    1. Error: setting an array element with a sequence.
    2. Error: only integer and so on are valid indices.
    Modify the DummyVecEnv.step_wait function to the following.
    """
    for env_idx in range(self.num_envs):
        env_action = np.trunc(self.actions[0])
        action = env_action.astype(int)
        result = self.envs[env_idx].step(action)
        obs = result[0]
        self.buf_rews[0] = np.sum(result[1])
        self.buf_dones[env_idx] = result[2]
        self.buf_infos[env_idx] = result[3]
        if self.buf_dones[env_idx]:
            self.buf_infos[env_idx]["terminal_observation"] = obs
            obs = self.envs[env_idx].reset()
        self._save_obs(env_idx, obs)
    return (self._obs_from_buf(), np.copy(self.buf_rews),
            np.copy(self.buf_dones), deepcopy(self.buf_infos))


def monitor_step(self, action: Union[np.ndarray, int]) -> GymStepReturn:
    """
    To deal with the error: numpy.ndarray doesn't define __round__ method.
    Modify the Monitor.step by changing the round() to np.round().
    """
    if self.needs_reset:
        raise RuntimeError("Tried to step environment that needs reset")
    observation, reward, done, info = self.env.step(action)
    self.rewards.append(reward)
    if done:
        self.needs_reset = True
        ep_rew = sum(self.rewards)
        ep_len = len(self.rewards)
        ep_info = {"r": np.round(ep_rew, 6), "l": ep_len,
                   "t": np.round(time.time() - self.t_start, 6)}
        for key in self.info_keywords:
            ep_info[key] = info[key]
        self.episode_returns.append(ep_rew)
        self.episode_lengths.append(ep_len)
        self.episode_times.append(time.time() - self.t_start)
        ep_info.update(self.current_reset_info)
        if self.results_writer:
            self.results_writer.write_row(ep_info)
        info["episode"] = ep_info
    self.total_steps += 1
    return observation, reward, done, info


def run():
    """
    Run this main function to do the changes in the stable-baselines3
    code.
    """
    SAC.__init__ = sac_init
    DummyVecEnv.step_wait = dummy_step_wait
    Monitor.step = monitor_step
