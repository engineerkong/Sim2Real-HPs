import pandas
import json
from omegaconf import DictConfig, OmegaConf, open_dict
import hydra
import wandb
import random
import pkg_resources
import os, time
import numpy as np
import matplotlib.pyplot as plt
import gym
import torch
import scipy
import myGym.envs
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common import results_plotter
from stable_baselines3 import PPO as PPO_P, A2C as A2C_P, SAC as SAC_P, TD3 as TD3_P

# Import helper classes and functions for monitoring
from myGym.utils.callbacks import ProgressBarManager, SaveOnBestTrainingRewardCallback,  CustomEvalCallback

# This is global variable for the type of engine we are working with
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
AVAILABLE_SIMULATION_ENGINES = ["pybullet"]
AVAILABLE_TRAINING_FRAMEWORKS = ["pytorch"]

def seed_everything(seed: int):
    """Set seeds for pytorch."""
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

def seed_rl_context(agent, seed) -> None:
    """Set seeds for a whole RL context (i.e., env and agent/policy)."""
    agent.env.seed(seed)
    agent.action_space.seed(seed)
    agent.action_space.np_random.seed(seed)
    agent.set_random_seed(seed)

def save_results(arg_dict, model_name, env, model_logdir=None, show=False):
    """Save the plot results."""
    if model_logdir is None:
        model_logdir = arg_dict["logdir"]
    print(f"model_logdir: {model_logdir}")

    results_plotter.EPISODES_WINDOW = 100
    results_plotter.plot_results([model_logdir], arg_dict["steps"], results_plotter.X_TIMESTEPS, arg_dict["algo"] + " " + arg_dict["env_name"] + " reward")
    plt.gcf().set_size_inches(8, 6)
    plt.savefig(os.path.join(model_logdir, model_name) + '_reward_results.png')
    #plot_extended_results(model_logdir, 'd', results_plotter.X_TIMESTEPS, arg_dict["algo"] + " " + arg_dict["env_name"] + " distance", "Episode Distances")
    plt.gcf().set_size_inches(8, 6)
    plt.savefig(os.path.join(model_logdir, model_name) + '_distance_results.png')
    plt.close()
    plt.close()
    results_plotter.plot_curves([(np.arange(len(env.unwrapped.episode_final_distance)),np.asarray(env.unwrapped.episode_final_distance))],'episodes',arg_dict["algo"] + " " + arg_dict["env_name"] + ' final step distance')
    plt.gcf().set_size_inches(8, 6)
    plt.ylabel("Step Distances")
    plt.savefig(os.path.join(model_logdir, model_name) + "_final_distance_results.png")
    plt.close()
    print("Congratulations! Training with {} timesteps succeed!".format(arg_dict["steps"]))
    if show:
        plt.show()

def configure_env(arg_dict, model_logdir=None, for_train=True):
    """Configure the environment using the given arguements in config file."""
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
                     "yolact_config": arg_dict["yolact_config"], "train_test": arg_dict["train_test"]}  
    env_arguments["gui_on"] = arg_dict["gui"]

    env = gym.make(arg_dict["env_name"], **env_arguments)
    if for_train:
        if arg_dict["engine"] == "mujoco":
            env = VecMonitor(env, model_logdir) if arg_dict["multiprocessing"] else Monitor(env, model_logdir)
        elif arg_dict["engine"] == "pybullet":
            env = Monitor(env, model_logdir, info_keywords=tuple('d'))
    return env


def configure_implemented_combos(env, model_logdir, arg_dict):
    """Configure the RL model."""
    implemented_combos = {"ppo":{"pytorch":[PPO_P, ('MlpPolicy', env), {"n_steps": 1024, "verbose": 1, "tensorboard_log": model_logdir}]},
                          "sac":{"pytorch":[SAC_P, ('MlpPolicy', env), {"verbose": 1, "tensorboard_log": model_logdir}]},
                          "td3":{"pytorch":[TD3_P, ('MlpPolicy', env), {"verbose": 1, "tensorboard_log": model_logdir}]},
                          "a2c":{"pytorch":[A2C_P, ('MlpPolicy', env), {"n_steps": arg_dict["algo_steps"], "verbose": 1, "tensorboard_log": model_logdir}]}}

    return implemented_combos

def train(env, implemented_combos, model_logdir, arg_dict, pretrained_model=None, seed=None):
    """Training process."""
    model_name = arg_dict["algo"] + '_' + str(arg_dict["steps"])
    conf_pth   = os.path.join(model_logdir, "train.json")
    model_path = os.path.join(model_logdir, "best_model.zip")
    with open_dict(arg_dict):
        arg_dict["model_path"] = model_path
    model_args = implemented_combos[arg_dict["algo"]][arg_dict["train_framework"]][1]
    model_kwargs = implemented_combos[arg_dict["algo"]][arg_dict["train_framework"]][2]
    if pretrained_model:
        if not os.path.isabs(pretrained_model):
            pretrained_model = pkg_resources.resource_filename("myGym", pretrained_model)
        env = model_args[1]
        # vec_env = DummyVecEnv([lambda: env])
        vec_env = env
        model = implemented_combos[arg_dict["algo"]][arg_dict["train_framework"]][0].load(pretrained_model, vec_env)
    else:
        model = implemented_combos[arg_dict["algo"]][arg_dict["train_framework"]][0](*model_args, **model_kwargs)
    seed_rl_context(model, seed=seed)

    start_time = time.time()
    callbacks_list = []
    if pretrained_model:
        model_logdir = pretrained_model.split('/')
        model_logdir = model_logdir[:-1]
        model_logdir = "/".join(model_logdir)
        auto_save_callback = SaveOnBestTrainingRewardCallback(check_freq=1024, logdir=model_logdir, env=env, engine=arg_dict["engine"], multiprocessing=arg_dict["multiprocessing"])
    else:
        auto_save_callback = SaveOnBestTrainingRewardCallback(check_freq=1024, logdir=model_logdir, env=env, engine=arg_dict["engine"], multiprocessing=arg_dict["multiprocessing"])
    callbacks_list.append(auto_save_callback)
    if arg_dict["eval_freq"]:
        #eval_env = configure_env(arg_dict, model_logdir, for_train=False)
        eval_env = env
        eval_callback = CustomEvalCallback(eval_env, log_path=model_logdir,
                                           eval_freq=arg_dict["eval_freq"],
                                           n_eval_episodes=arg_dict["eval_episodes"],
                                           record=arg_dict["record"],
                                           camera_id=arg_dict["camera"])
        callbacks_list.append(eval_callback)
    # callbacks_list.append(PlottingCallback(model_logdir))
    with ProgressBarManager(total_timesteps=arg_dict["steps"]) as progress_callback:
        callbacks_list.append(progress_callback)
        model.learn(total_timesteps=arg_dict["steps"], callback=callbacks_list)
    model.save(os.path.join(model_logdir, model_name))
    if arg_dict["algo"] == "sac":
        model.save_replay_buffer(os.path.join(model_logdir,"replay_buffer.pkl"))
    print(os.path.join(model_logdir, 'model_torch.pth.tar'))
    torch.save(model.get_parameters(), os.path.join(model_logdir, 'model_torch.pth.tar'), _use_new_zipfile_serialization=False)
    print("Training time: {:.2f} s".format(time.time() - start_time))

    # info_keywords in monitor class above is neccessary for pybullet to save_results
    # when using the info_keywords for mujoco we get an error
    if arg_dict["engine"] == "pybullet":
        save_results(arg_dict, model_name, env, model_logdir)
    return model

def test(env, implemented_combos, model_logdir, arg_dict, pretrained_model=None, seed=None, eval_episodes=0, eval_steps=0):
    """Testing process."""
    model_args = implemented_combos[arg_dict["algo"]][arg_dict["train_framework"]][1]
    model_kwargs = implemented_combos[arg_dict["algo"]][arg_dict["train_framework"]][2]

    csv_file = get_csv_path(pretrained_model)
    env = model_args[1]
    vec_env = env
    if arg_dict["algo"] == "sac":
        model = SAC_P("MlpPolicy", vec_env)
    elif arg_dict["algo"] == "ppo":
        model = PPO_P("MlpPolicy", vec_env)
    params = torch.load(pretrained_model)
    for name in params:
        attr = None
        attr = recursive_getattr(model, name)
        attr.load_state_dict(params[name])
    seed_rl_context(model, seed=seed)
    sum_list = []
    iqm_list = []
    len_list = []
    for i in range(eval_episodes):
        obs = env.reset()
        for j in range(eval_steps):
            action = model.predict(obs)
            obs, reward, done, info = env.step(action[0])
            if done:
                break
        episode_iqm_reward = scipy.stats.trim_mean(np.array(env.episode_reward_list), proportiontocut=0.25, axis=None)
        sum_list.append(env.episode_reward)
        iqm_list.append(episode_iqm_reward)
        len_list.append(len(env.episode_reward_list))
    dict_sim = {"sum":sum_list, "iqm":iqm_list, "len":len_list}
    str_sim = json.dumps(dict_sim)
    df = pandas.read_csv(csv_file)
    new_column_df = pandas.DataFrame({'eval_seed': seed}, index=df.index)
    new_df = pandas.concat([df, new_column_df], axis=1)
    newnew_column_df = pandas.DataFrame({'sim': [str_sim]}, index=new_df.index)
    newnew_df = pandas.concat([new_df, newnew_column_df], axis=1)
    newnew_df.to_csv(csv_file, index=False)
    del model


import functools
def recursive_getattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split("."))

def search_files(folder_path, target_file_extension):
    target_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(target_file_extension):
                file_path = os.path.join(root, file)
                target_files.append(file_path)
    return target_files

def get_csv_path(model_path):
    parent_dir = os.path.dirname(model_path)
    csv_path = os.path.join(parent_dir,"data.csv")
    return csv_path
    
@hydra.main(version_base=None, config_path="configs", config_name="config")
def main(cfg: DictConfig):
    # handle configs
    dict_cfg = OmegaConf.to_container(cfg, resolve=True, enum_to_str=True)
    arg_dict = cfg["task"]
    tes = cfg["test"]
    OmegaConf.set_struct(arg_dict, True)
    
    # Check if we chose one of the existing engines
    if arg_dict["engine"] not in AVAILABLE_SIMULATION_ENGINES:
        print(f"Invalid simulation engine. Valid arguments: --engine {AVAILABLE_SIMULATION_ENGINES}.")
        return
            
    # handle seeds    
    seed = np.random.randint(10000)
    print(f"seed:{seed}")
    
    # handle model logdir
    if not os.path.isabs(arg_dict["logdir"]):
        with open_dict(arg_dict):
            arg_dict["logdir"] = os.path.join("./", arg_dict["logdir"])
    os.makedirs(arg_dict["logdir"], exist_ok=True)
    if tes:
        ttname = "test"
    else: 
        ttname = "train"
    model_logdir_ori = os.path.join(arg_dict["logdir"], "_".join((ttname,arg_dict["reward"],arg_dict["algo"],str(seed))))
    model_logdir = model_logdir_ori
    add = 2
    while True:
        try:
            os.makedirs(model_logdir, exist_ok=False)
            break
        except:
            model_logdir = "_".join((model_logdir_ori, str(add)))
            add += 1
    
    if not tes:
        # build env and start train
        env = configure_env(arg_dict, model_logdir, 1) # train: Monitor
        implemented_combos = configure_implemented_combos(env, model_logdir, arg_dict)
        with wandb.init(
            mode="online",
            project="se1_test",
            tags="train",
            dir=os.getcwd(),
            config=dict_cfg,
        ):
            seed_everything(seed=seed)
            train(env, implemented_combos, model_logdir, arg_dict, arg_dict["pretrained_model"], seed)
        print(model_logdir)
    else:
        eval_episodes = 10
        eval_steps = 10
        folder_path = "/home/lingxiao/Desktop/docker_se1/src/mygym/myGym/trained_models/"
        # load env and start test
        target_file_extension = '.pth.tar'
        pretrained_models = search_files(folder_path, target_file_extension)
        for pretrained_model in pretrained_models:
            env = configure_env(arg_dict, model_logdir, 0) # train: Monitor
            implemented_combos = configure_implemented_combos(env, model_logdir, arg_dict)
            with wandb.init(
                mode="online",
                project="se1_test",
                tags="test",
                dir=os.getcwd(),
                config=dict_cfg,
            ):
                seed_everything(seed=seed)
                test(env, implemented_combos, model_logdir, arg_dict, pretrained_model, seed, eval_episodes, eval_steps)
            del env

if __name__ == "__main__":

    main()
