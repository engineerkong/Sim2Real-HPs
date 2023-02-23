import gym
import numpy as np
import torch
from mod_sb3 import run
from stable_baselines3 import SAC
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise
from stable_baselines3.sac.policies import CnnPolicy, MlpPolicy, MultiInputPolicy, SACPolicy

run()

print("-------------train--------------")
env = gym.make("Pendulum-v0")
n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))
model = SAC("MlpPolicy", env, action_noise=action_noise, verbose=1) # reset policy
model.learn(total_timesteps=1000, log_interval=10)

torch.save(model.get_parameters(), 'model_torch.pth.tar', _use_new_zipfile_serialization=False)
del model # remove to demonstrate saving and loading
env.close()