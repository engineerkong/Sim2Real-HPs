from robogym.utils.env_utils import load_env
from ned2_wrapper import Ned2_Wrapper
from stable_baselines3 import DDPG
import matplotlib.pyplot as plt
from mod_sb3 import run

# train on sim env
names = 'robogym_wrapper.py'
kwargs = {'parameters': {'simulation_params': {'num_objects': 1}}}
sim_env, args_remaining = load_env(names, return_args_remaining=True, **kwargs)
run()
model = DDPG("MultiInputPolicy", sim_env)
model.learn(total_timesteps=100000, log_interval=10)

# deploy on real env
real_env = Ned2_Wrapper("10.10.10.10", model, 100, 100)
list_num_eval, list_reward = real_env.eval()

# plot
fig, ax = plt.subplots()
ax.set(list_num_eval, list_reward)
plt.show()
