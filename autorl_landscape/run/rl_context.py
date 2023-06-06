import gym
from stable_baselines3.common.base_class import BaseAlgorithm
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.monitor import Monitor
from myGym import envs

def make_env(env_name: str, seed: int, n_envs = None) -> gym.Env:
    """Quick helper to create a gym env and seed it."""
    if n_envs is not None:
        env = make_vec_env(env_name, n_envs, seed)
    else:
        env = gym.make(env_name)
        env = Monitor(env)
        env.seed(seed)
    return env

def make_env_mygym(env_name: str, seed: int, n_envs = None, arg_dict = {}) -> gym.Env:
    """Quick helper to create a gym env and seed it."""
    env_arguments = {"render_on": True, "visualize": arg_dict["visualize"], "workspace": arg_dict["workspace"],
                     "robot": arg_dict["robot"], "robot_init_joint_poses": arg_dict["robot_init"],
                     "robot_action": arg_dict["robot_action"],"max_velocity": arg_dict["max_velocity"], 
                     "max_force": arg_dict["max_force"],"task_type": arg_dict["task_type"],
                     "action_repeat": arg_dict["action_repeat"], "task_objects":arg_dict["task_objects"], 
                     "observation":arg_dict["observation"], "distractors":arg_dict["distractors"],
                     "num_networks":arg_dict.get("num_networks", 1), "network_switcher":arg_dict.get("network_switcher", "gt"),
                     "distance_type": arg_dict["distance_type"], "used_objects": arg_dict["used_objects"],
                     "active_cameras": arg_dict["camera"], "use_ee_camera": arg_dict["ee_camera"],
                     "color_dict":arg_dict.get("color_dict", {}), "max_steps": arg_dict["max_episode_steps"], 
                     "visgym":arg_dict["visgym"], "reward": arg_dict["reward"], "logdir": arg_dict["logdir"], 
                     "vae_path": arg_dict["vae_path"], "yolact_path": arg_dict["yolact_path"], 
                     "yolact_config": arg_dict["yolact_config"], "train_test": arg_dict["train_test"], "gui_on": arg_dict["gui"]}
    if n_envs is not None:
        env = make_vec_env(env_name, n_envs, seed)
    else:
        env = gym.make(env_name, **env_arguments)
        env = Monitor(env)
        env.seed(seed)
    return env

def seed_rl_context(agent: BaseAlgorithm, seed: int, reset: bool = False) -> None:
    """Set seeds for a whole RL context (i.e., env and agent/policy)."""
    agent.env.seed(seed)
    agent.action_space.seed(seed)
    agent.action_space.np_random.seed(seed)
    agent.set_random_seed(seed)
    if reset:
        agent.env.reset()
