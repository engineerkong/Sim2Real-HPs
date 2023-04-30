"""Abstract base classes for RL algorithms."""

import gym
import torch as th

from sb3_py3.vec_env import (
    DummyVecEnv,
    VecEnv,
    VecTransposeImage,
    is_vecenv_wrapped,
    unwrap_vec_normalize,
)
from sb3_py3.preprocessing import check_for_nested_spaces, is_image_space, is_image_space_channels_first
from sb3_py3.monitor import Monitor
from sb3_py3.env_util import is_wrapped
from sb3_py3.base_policies import get_policy_from_name
from sb3_py3.utils import get_device, get_schedule_fn, set_random_seed

def maybe_make_env(env, verbose):
    """If env is a string, make the environment; otherwise, return env.

    :param env: The environment to learn from.
    :param verbose: logging verbosity
    :return A Gym (vector) environment.
    """
    if isinstance(env, str):
        if verbose >= 1:
            print(f"Creating environment from the given name '{env}'")
        env = gym.make(env)
    return env

class BaseAlgorithm:

    def __init__(
        self,
        policy,
        env,
        policy_base,
        learning_rate,
        policy_kwargs = None,
        tensorboard_log = None,
        verbose = 0,
        device = "auto",
        support_multi_env = False,
        create_eval_env = False,
        monitor_wrapper = True,
        seed = None,
        use_sde = False,
        sde_sample_freq = -1,
        supported_action_spaces = None,
    ):
        if isinstance(policy, str) and policy_base is not None:
            self.policy_class = get_policy_from_name(policy_base, policy)
        else:
            self.policy_class = policy
        self.device = get_device(device)
        if verbose > 0:
            print(f"Using {self.device} device")
        self.env = None
        self._vec_normalize_env = unwrap_vec_normalize(env)
        self.verbose = verbose
        self.policy_kwargs = {} if policy_kwargs is None else policy_kwargs
        self.observation_space = None
        self.action_space = None
        self.n_envs = None
        self.num_timesteps = 0
        self._total_timesteps = 0
        self.eval_env = None
        self.seed = seed
        self.action_noise = None
        self.start_time = None
        self.policy = None
        self.learning_rate = learning_rate
        self.tensorboard_log = tensorboard_log
        self.lr_schedule = None
        self._last_obs = None
        self._last_episode_starts = None
        self._last_original_obs = None
        self._episode_num = 0
        self.use_sde = use_sde
        self.sde_sample_freq = sde_sample_freq
        self._current_progress_remaining = 1
        self.ep_info_buffer = None
        self.ep_success_buffer = None
        self._n_updates = 0
        self._logger = None
        self._custom_logger = False
        if env is not None:
            if isinstance(env, str):
                if create_eval_env:
                    self.eval_env = maybe_make_env(env, self.verbose)
            env = maybe_make_env(env, self.verbose)
            env = self._wrap_env(env, self.verbose, monitor_wrapper)
            self.observation_space = env.observation_space
            self.action_space = env.action_space
            self.n_envs = env.num_envs
            self.env = env
            if supported_action_spaces is not None:
                assert isinstance(self.action_space, supported_action_spaces), (
                    f"The algorithm only supports {supported_action_spaces} as action spaces "
                    f"but {self.action_space} was provided"
                )
            if not support_multi_env and self.n_envs > 1:
                raise ValueError(
                    "Error: the model does not support multiple envs; it requires " "a single vectorized environment."
                )
            if self.use_sde and not isinstance(self.action_space, gym.spaces.Box):
                raise ValueError("generalized State-Dependent Exploration (gSDE) can only be used with continuous actions.")

    @staticmethod
    def _wrap_env(env, verbose = 0, monitor_wrapper = True):
        if not isinstance(env, VecEnv):
            if not is_wrapped(env, Monitor) and monitor_wrapper:
                if verbose >= 1:
                    print("Wrapping the env with a `Monitor` wrapper")
                env = Monitor(env)
            if verbose >= 1:
                print("Wrapping the env in a DummyVecEnv.")
            env = DummyVecEnv([lambda: env])
        check_for_nested_spaces(env.observation_space)
        if isinstance(env.observation_space, gym.spaces.Dict):
            for space in env.observation_space.spaces.values():
                if isinstance(space, gym.spaces.Dict):
                    raise ValueError("Nested observation spaces are not supported (Dict spaces inside Dict space).")
        if not is_vecenv_wrapped(env, VecTransposeImage):
            wrap_with_vectranspose = False
            if isinstance(env.observation_space, gym.spaces.Dict):
                for space in env.observation_space.spaces.values():
                    wrap_with_vectranspose = wrap_with_vectranspose or (
                        is_image_space(space) and not is_image_space_channels_first(space)
                    )
            else:
                wrap_with_vectranspose = is_image_space(env.observation_space) and not is_image_space_channels_first(
                    env.observation_space
                )
            if wrap_with_vectranspose:
                if verbose >= 1:
                    print("Wrapping the env in a VecTransposeImage.")
                env = VecTransposeImage(env)
        return env

    def _setup_lr_schedule(self):
        self.lr_schedule = get_schedule_fn(self.learning_rate)


    def predict(
        self,
        observation,
        state = None,
        mask = None,
        deterministic = False,
    ):
        return self.policy.predict(observation, state, mask, deterministic)

    def set_random_seed(self, seed = None):
        if seed is None:
            return
        set_random_seed(seed, using_cuda=self.device.type == th.device("cuda").type)
        self.action_space.seed(seed)
        if self.env is not None:
            self.env.seed(seed)
        if self.eval_env is not None:
            self.eval_env.seed(seed)
