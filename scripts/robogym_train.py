from robogym.utils.env_utils import load_env
from stable_baselines3 import SAC
from Sim2Real_py3.sb3_wrapper import run
import torch

# train on sim env
names = './Sim2Real_py3/robogym_wrapper.py'
kwargs = {'parameters': {'simulation_params': {'num_objects': 1}}}
sim_env, args_remaining = load_env(names, return_args_remaining=True, **kwargs)
run()
model = SAC("MultiInputPolicy", sim_env)
model.learn(total_timesteps=1000, log_interval=10)

torch.save(model.get_parameters(), 'model_robogym_torch.pth.tar', _use_new_zipfile_serialization=False)
del model # remove to demonstrate saving and loading
sim_env.close()