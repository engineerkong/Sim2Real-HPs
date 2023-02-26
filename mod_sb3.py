from stable_baselines3.sac.sac import SAC
from stable_baselines3.td3.td3 import TD3
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union
import gym
import time
import numpy as np
import torch as th
from torch.nn import functional as F
from copy import deepcopy
from stable_baselines3.common.buffers import ReplayBuffer
from stable_baselines3.common.noise import ActionNoise
from stable_baselines3.common.type_aliases import GymEnv, MaybeCallback, Schedule
from stable_baselines3.common.utils import get_parameters_by_name, polyak_update
from stable_baselines3.td3.policies import CnnPolicy, MlpPolicy, MultiInputPolicy, TD3Policy
from stable_baselines3.common.vec_env.base_vec_env import VecEnv, VecEnvIndices, VecEnvObs, VecEnvStepReturn
from stable_baselines3.common.type_aliases import GymObs, GymStepReturn
from stable_baselines3.sac.policies import SACPolicy, Actor
from stable_baselines3.sac.policies import CnnPolicy, MlpPolicy, MultiInputPolicy, SACPolicy
from robogym.envs.rearrange.common.base import RearrangeEnv

def _observe_simple_test(self):
        """
        Default observation for the environment. An observation can be added here if
        it meets one of the condition below:

        1. It's cheap to fetch on a per step basic and doesn't cause side effect even
            if not used by policy.
        2. It's shared across all variances of the env.
        """

        robot_obs = self.mujoco_simulation.robot.observe()

        obs = {
            "obj_pos": self.mujoco_simulation.get_object_pos(),
            "obj_rel_pos": self.mujoco_simulation.get_object_rel_pos(),
            "obj_vel_pos": self.mujoco_simulation.get_object_vel_pos(),
            "obj_rot": self.mujoco_simulation.get_object_rot(),
            "obj_vel_rot": self.mujoco_simulation.get_object_vel_rot(),
            "robot_joint_pos": robot_obs.joint_positions(),
            "gripper_pos": robot_obs.tcp_xyz(),
            "gripper_velp": robot_obs.tcp_vel(),
            "gripper_controls": robot_obs.gripper_controls(),
            "gripper_qpos": robot_obs.gripper_qpos(),
            "gripper_vel": robot_obs.gripper_vel(),
            "qpos": self.mujoco_simulation.qpos,
            "qpos_goal": self._goal["qpos_goal"].copy(),
            "goal_obj_pos": self._goal["obj_pos"].copy(),
            "goal_obj_rot": self._goal["obj_rot"].copy(),
            "is_goal_achieved": np.array([self._is_goal_achieved], np.int32),
            "rel_goal_obj_pos": self._goal_info_dict["rel_goal_obj_pos"].copy(),
            "rel_goal_obj_rot": self._goal_info_dict["rel_goal_obj_rot"].copy(),
            "obj_gripper_contact": self.mujoco_simulation.get_object_gripper_contact(),
            "obj_bbox_size": self.mujoco_simulation.get_object_bounding_box_sizes(),
            "obj_colors": self.mujoco_simulation.get_object_colors(),
            "safety_stop": np.array([robot_obs.is_in_safety_stop()]),
            "tcp_force": robot_obs.tcp_force(),
            "tcp_torque": robot_obs.tcp_torque(),
        }

        if self.constants.mask_obs_outside_placement_area:
            obs = self._mask_goal_observation(
                obs, self._goal["goal_objects_in_placement_area"].copy()
            )
            obs = self._mask_object_observation(obs)

        return obs

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
    self.log_ent_coef = None  # type: Optional[th.Tensor]
    # Entropy coefficient / Entropy temperature
    # Inverse of the reward scale
    self.ent_coef = ent_coef
    self.target_update_interval = target_update_interval
    self.ent_coef_optimizer = None

    if _init_setup_model:
        self._setup_model()

def td3_init(
        self,
        policy: Union[str, Type[TD3Policy]],
        env: Union[GymEnv, str],
        learning_rate: Union[float, Schedule] = 1e-3,
        buffer_size: int = 1_000_000,  # 1e6
        learning_starts: int = 100,
        batch_size: int = 100,
        tau: float = 0.005,
        gamma: float = 0.99,
        train_freq: Union[int, Tuple[int, str]] = (1, "episode"),
        gradient_steps: int = -1,
        action_noise: Optional[ActionNoise] = None,
        replay_buffer_class: Optional[Type[ReplayBuffer]] = None,
        replay_buffer_kwargs: Optional[Dict[str, Any]] = None,
        optimize_memory_usage: bool = False,
        policy_delay: int = 2,
        target_policy_noise: float = 0.2,
        target_noise_clip: float = 0.5,
        tensorboard_log: Optional[str] = None,
        create_eval_env: bool = False,
        policy_kwargs: Optional[Dict[str, Any]] = None,
        verbose: int = 0,
        seed: Optional[int] = None,
        device: Union[th.device, str] = "auto",
        _init_setup_model: bool = True,
):
    super(TD3, self).__init__(
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
        action_noise=action_noise,
        replay_buffer_class=replay_buffer_class,
        replay_buffer_kwargs=replay_buffer_kwargs,
        policy_kwargs=policy_kwargs,
        tensorboard_log=tensorboard_log,
        verbose=verbose,
        device=device,
        seed=seed,
        sde_support=False,
        optimize_memory_usage=optimize_memory_usage,
        # Error: only supports <class 'gym.spaces.box.Box'>. Deal: modify from Box to Space
        supported_action_spaces=(gym.spaces.Space),
        support_multi_env=True,
    )
    self.policy_delay = policy_delay
    self.target_noise_clip = target_noise_clip
    self.target_policy_noise = target_policy_noise

    if _init_setup_model:
        self._setup_model()

def td3_train(self, gradient_steps: int, batch_size: int = 100) -> None:
    # Switch to train mode (this affects batch norm / dropout)
    self.policy.set_training_mode(True)

    # Update learning rate according to lr schedule
    self._update_learning_rate([self.actor.optimizer, self.critic.optimizer])

    actor_losses, critic_losses = [], []

    for _ in range(gradient_steps):

        self._n_updates += 1
        # Sample replay buffer
        replay_data = self.replay_buffer.sample(batch_size, env=self._vec_normalize_env)

        with th.no_grad():
            # Select action according to policy and add clipped noise
            # Error: replay_data.actions is Long. data.normal_ must not be Long? But actions must be Long?
            # Deal: following
            actions_float = replay_data.actions.float()
            noise = actions_float.clone().data.normal_(0., self.target_policy_noise)
            noise = noise.clamp(-self.target_noise_clip, self.target_noise_clip)
            next_actions = (self.actor_target(replay_data.next_observations) + noise).clamp(-1, 1)

            # Compute the next Q-values: min over all critics targets
            next_q_values = th.cat(self.critic_target(replay_data.next_observations, next_actions), dim=1)
            next_q_values, _ = th.min(next_q_values, dim=1, keepdim=True)
            target_q_values = replay_data.rewards + (1 - replay_data.dones) * self.gamma * next_q_values

        # Get current Q-values estimates for each critic network
        current_q_values = self.critic(replay_data.observations, replay_data.actions)

        # Compute critic loss
        critic_loss = sum(F.mse_loss(current_q, target_q_values) for current_q in current_q_values)
        critic_losses.append(critic_loss.item())

        # Optimize the critics
        self.critic.optimizer.zero_grad()
        critic_loss.backward()
        self.critic.optimizer.step()

        # Delayed policy updates
        if self._n_updates % self.policy_delay == 0:
            # Compute actor loss
            actor_loss = -self.critic.q1_forward(replay_data.observations, self.actor(replay_data.observations)).mean()
            actor_losses.append(actor_loss.item())

            # Optimize the actor
            self.actor.optimizer.zero_grad()
            actor_loss.backward()
            self.actor.optimizer.step()

            polyak_update(self.critic.parameters(), self.critic_target.parameters(), self.tau)
            polyak_update(self.actor.parameters(), self.actor_target.parameters(), self.tau)
            # Copy running stats, see GH issue #996
            polyak_update(self.critic_batch_norm_stats, self.critic_batch_norm_stats_target, 1.0)
            polyak_update(self.actor_batch_norm_stats, self.actor_batch_norm_stats_target, 1.0)

    self.logger.record("train/n_updates", self._n_updates, exclude="tensorboard")
    if len(actor_losses) > 0:
        self.logger.record("train/actor_loss", np.mean(actor_losses))
    self.logger.record("train/critic_loss", np.mean(critic_losses))
    
def dummy_step_wait(self) -> VecEnvStepReturn:
    # Error: setting an array element with a sequence. Deal: following
    for env_idx in range(self.num_envs):
        # Error: only integer and so on are valid indices. Deal: following
        env_action = np.trunc(self.actions[0])
        action = env_action.astype(int)
        result = self.envs[env_idx].step(
            action
        )
        obs = result[0]
        self.buf_rews[0] = np.sum(result[1])
        self.buf_dones[env_idx] = result[2]
        self.buf_infos[env_idx] = result[3]
        if self.buf_dones[env_idx]:
            # save final observation where user can get it, then reset
            self.buf_infos[env_idx]["terminal_observation"] = obs
            obs = self.envs[env_idx].reset()
        self._save_obs(env_idx, obs)
    return (self._obs_from_buf(), np.copy(self.buf_rews), np.copy(self.buf_dones), deepcopy(self.buf_infos))


def monitor_step(self, action: Union[np.ndarray, int]) -> GymStepReturn:
    """
    Step the environment with the given action

    :param action: the action
    :return: observation, reward, done, information
    """
    if self.needs_reset:
        raise RuntimeError("Tried to step environment that needs reset")
    observation, reward, done, info = self.env.step(action)
    self.rewards.append(reward)
    if done:
        self.needs_reset = True
        ep_rew = sum(self.rewards)
        ep_len = len(self.rewards)
        ep_info = {"r": np.round(ep_rew, 6), "l": ep_len, "t": np.round(time.time() - self.t_start, 6)}
        # Error: numpy.ndarray doesn't define __round__ method. Deal: change round to np.round
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

    RearrangeEnv._observe_simple = _observe_simple_test
    SAC.__init__ = sac_init
    TD3.__init__ = td3_init
    TD3.train = td3_train
    DummyVecEnv.step_wait = dummy_step_wait
    Monitor.step = monitor_step