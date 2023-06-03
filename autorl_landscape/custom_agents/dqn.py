from __future__ import annotations

from typing import Any, List, Dict, Tuple, Set

import pickle
from pathlib import Path

from stable_baselines3.common.type_aliases import MaybeCallback
from stable_baselines3.common.utils import constant_fn, get_linear_fn
from stable_baselines3.dqn.dqn import DQN

from autorl_landscape.custom_agents.off_policy_algorithm import custom_learn
from autorl_landscape.run.rl_context import seed_rl_context


class CustomDQN(DQN):
    """Slightly changed DQN Agent that can be saved and loaded at any point to reproduce learning exactly."""

    def learn(
        self,
        total_timesteps: int,
        callback: MaybeCallback = None,
        log_interval: int = 4,
        tb_log_name: str = "DQN",
        reset_num_timesteps: bool = True,
        progress_bar: bool = False,
    ) -> CustomDQN:
        """Like original method from `OffPolicyAlgorithm`, but call `after_update()` callback method."""
        return custom_learn(
            self, total_timesteps, callback, log_interval, tb_log_name, reset_num_timesteps, progress_bar
        )

    @classmethod
    def custom_load(cls, save_path: Path, seed: int) -> CustomDQN:
        """Load agent which will perform deterministically with further training, like the originally saved agent."""
        loaded_agent: CustomDQN = CustomDQN.load(save_path / Path("model.zip"))
        loaded_agent.load_replay_buffer(save_path / Path("replay_buffer.pkl"))
        with open(save_path / Path("env.pkl"), "rb") as f:
            loaded_agent.set_env(pickle.load(f), force_reset=False)
        seed_rl_context(loaded_agent, seed)
        return loaded_agent

    def custom_save(self, save_path: str, seed: int) -> None:
        """Save the agent so that it will perform deterministically with further training.

        Can be loaded afterwards with `custom_load`.
        """
        # re-seed the original agent to allow for same results with the loaded agent
        seed_rl_context(self, seed)

        self.save(f"{save_path}/model.zip")
        self.save_replay_buffer(f"{save_path}/replay_buffer.pkl")
        with open(f"{save_path}/env.pkl", "wb") as f:
            e = self.get_env()
            pickle.dump(e, f)

    def set_ls_conf(self, ls_spec: Dict[str, Any], phase_index: int) -> None:
        """Set up the agent with the wanted configuration. Special handling for learning rate and exploration."""
        for hp_name, hp_val in ls_spec.items():
            # First, handle special cases:
            if [hp_name, phase_index] == ["exploration_final_eps", 1]:
                    # In the first phase, set up the default linear schedule:
                    self.exploration_schedule = get_linear_fn(
                        self.exploration_initial_eps, hp_val, self.exploration_fraction
                    )
            elif hp_name == "exploration_final_eps":
                    # In subsequent phases, use a constant schedule:
                    self.exploration_schedule = constant_fn(hp_val)
            elif hp_name == "learning_rate":
                    self.lr_schedule = constant_fn(hp_val)
                # Then, the rest:
            else:
                    if not hasattr(self, hp_name):
                        error_msg = f"Hyperparameter {hp_name} cannot be set for {type(self)}."
                        raise ValueError(error_msg)
                    setattr(self, hp_name, hp_val)

    def get_ls_conf(self, ls_spec: List[str]) -> Dict[str, Any]:
        """Read the actually used hyperparameter configuration.

        Args:
            ls_spec: list of hyperparameters to read (should come from the hydra config)
        """
        ls_conf: Dict[str, Any] = {}
        for hp_name in ls_spec:
            if hp_name == "exploration_final_eps":
                    ls_conf["exploration_rate"] = self.exploration_rate
            elif hp_name == "learning_rate":
                    ls_conf["learning_rate"] = self.lr_schedule(self._current_progress_remaining)
            else:
                    if not hasattr(self, hp_name):
                        error_msg = f"Hyperparameter {hp_name} does not exist for {type(self)}."
                        raise ValueError(error_msg)
                    ls_conf[hp_name] = getattr(self, hp_name)
        return ls_conf
