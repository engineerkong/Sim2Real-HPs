#!/usr/bin/env python

# Imports
from niryo_robot_python_ros_wrapper.ros_wrapper_mygym import *
# from detection_improve import detection_improve
import torch
import functools
from sb3_py2.ppo_algorithm import PPO
from sb3_py2.sac_algorithm import SAC
from sb3_py2.ppo_policy import MlpPolicy as PPO_MlpPolicy
from sb3_py2.sac_policy import MlpPolicy as SAC_MlpPolicy
from gym.spaces import Box
import rospy
from std_srvs.srv import Empty
import random
import numpy as np
import pandas
import wandb
import os
import json
import time
from gazebo_msgs.msg import ModelState 
from gazebo_msgs.srv import SetModelState

def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

def seed_rl_context(agent, seed):
    """Set seeds for a whole RL context (i.e., env and agent/policy)."""
    agent.env.seed(seed)
    agent.action_space.seed(seed)
    agent.action_space.np_random.seed(seed)
    agent.set_random_seed(seed)

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
    
def get_random_object_position(boarders):
    """
    Generate random position in defined volume

    Parameters:
        :param boarders: (list) Volume, where position may be generated ([x,x,y,y,z,z])
    Returns:
        :return pos: (list) Position in specified volume ([x,y,z])
    """
    if any(isinstance(i, list) for i in boarders):
        boarders = boarders[random.randint(0,len(boarders)-1)]
    pos = []
    pos.append(random.uniform(boarders[0], boarders[1])) #x
    pos.append(random.uniform(boarders[2], boarders[3])) #y
    pos.append(random.uniform(boarders[4], boarders[5])) #z
    return pos
    
def reset_world():
    reset_proxy = rospy.ServiceProxy("/gazebo/reset_world", Empty)
    try:
        reset_proxy()

    except rospy.ServiceException as e:
        print("/gazebo/reset_simulation service call failed")

def reset_object():
    rospy.wait_for_service('/gazebo/set_model_state')
    try:
        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
    
    except rospy.ServiceException :
        print("Service call failed")

    state_msg = ModelState()
    state_msg.model_name = 'cube_blue'

    pos=get_random_object_position([0.2,0.3,-0.1,0.1,0.012,0.012])
    state_msg.pose.position.x =  pos[0]
    state_msg.pose.position.y = pos[1]
    state_msg.pose.position.z =  pos[2]
    state_msg.pose.orientation.w = 1
    state_msg.pose.orientation.x = 0
    state_msg.pose.orientation.y = 0
    state_msg.pose.orientation.z = 0
    resp = set_state(state_msg)
    return pos

class MygymEnv:

    def __init__(self):
        
        self.observation_space = Box(-float('inf'), float('inf'), (13,))
        self.action_space = Box(-float(1), float(1), (6,))
        self.action_space.high = np.array([2.99987191833, 0.610167106497, 1.57009819509, 2.09003177926, 1.92282923692, 2.53002928369])
        self.action_space.low = np.array([-2.99987191833, -1.83259571459, -1.34006379968, -2.09003177926, -1.92003671012, -2.53002928369])
        self.reward_range = (-float('inf'), float('inf'))
        self.metadata = {}

def eval(dummy_env=None, ros_env=None, algo=None, pretrained_model=None, eval_episodes=0, eval_steps=0):
    print(pretrained_model)
    csv_file = get_csv_path(pretrained_model)
    print(csv_file)
    df_check = pandas.read_csv(csv_file)
    if "real" not in df_check.columns:
        seed = df_check["eval_seed"].iloc[0]
        print("seed:{}".format(seed))
        sim = df_check["sim"].iloc[0]
        print("sim:{}".format(sim))
        seed_everything(seed=seed)
        if algo == "sac":
            model = SAC(SAC_MlpPolicy, dummy_env)
        elif algo == "ppo":
            model = PPO(PPO_MlpPolicy, dummy_env)
        params = torch.load(pretrained_model)
        for name in params:
            attr = None
            attr = recursive_getattr(model, name)
            attr.load_state_dict(params[name])
        # seed_rl_context(model, seed=seed) # TODO
        sum_list = []
        iqm_list = []
        len_list = []
        for i in range(eval_episodes):
            time.sleep(1)
            reset_world()
            obj_pos = reset_object()
            time.sleep(1)
            obs = ros_env.reset()
            for j in range(eval_steps):
                action = model.predict(obs)
                obs, reward, finish = ros_env.step(action[0])
                if finish:
                    break
            sum_list.append(ros_env.episode_reward)
            iqm_list.append(ros_env.episode_iqm_reward)
            len_list.append(len(ros_env.episode_reward_list))
        dict_real = {"sum":sum_list, "iqm":iqm_list, "len":len_list}
        str_real = json.dumps(dict_real)
        df = pandas.read_csv(csv_file)
        new_column_df = pandas.DataFrame({'real': [str_real]}, index=df.index)
        new_df = pandas.concat([df, new_column_df], axis=1)
        new_df.to_csv(csv_file, index=False)
        del model, ros_env

def main():
    # Initializing ROS node
    rospy.init_node('niryo_robot_example_python_ros_wrapper')
    # handle configs
    folder_path = "/home/lingxiao/master/ppo_nocollision"
    eval_episodes= 10
    eval_steps = 10
    task = "reach"
    algo = "ppo"
    sampling_area = [0.15,0.35,-0.15,0.15,0.012,0.012]
    # start evaluation
    target_file_extension = '.pth.tar'
    pretrained_models = search_files(folder_path, target_file_extension)
    # build env
    dummy_env = MygymEnv()
    ros_env = NiryoRosWrapperMygym(dummy_env, task, sampling_area, eval_steps)
    for pretrained_model in pretrained_models:
        with wandb.init(
            mode="disabled",
            project="ros_eval_reach",
            tags="test1",
            dir=os.getcwd(),
        ):
            eval(dummy_env, ros_env, algo, pretrained_model, eval_episodes, eval_steps)

if __name__ == "__main__":
    main()