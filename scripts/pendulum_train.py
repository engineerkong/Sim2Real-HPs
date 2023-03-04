import gym
import numpy as np
import torch
from stable_baselines3 import SAC
from stable_baselines3.common.noise import NormalActionNoise

from Sim2Real_py3.sb3_wrapper import run

if __name__ == "__main__":
    """
    The main function to train a policy on the gym environment
    Pendulum based on the sac algorithm and MlpPolicy in
    stable-baselines3.
    """

    print("-------------train--------------")

    # sb3 wrapper
    run()  # sb3 wrapper

    # train model from env
    env = gym.make("Pendulum-v0")
    n_actions = env.action_space.shape[-1]
    action_noise = NormalActionNoise(mean=np.zeros(n_actions),
                                     sigma=0.1 * np.ones(n_actions))
    model = SAC("MlpPolicy", env, action_noise=action_noise, verbose=1)
    model.learn(total_timesteps=10000, log_interval=10)

    # save model and delete
    torch.save(model.get_parameters(), "model_torch.pth.tar",
               _use_new_zipfile_serialization=False)
    del model  # remove to demonstrate saving and loading
    env.close()
