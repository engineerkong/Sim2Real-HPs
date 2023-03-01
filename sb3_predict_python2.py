import gym
import numpy as np
import torch
import functools
from sb3_python2.model import Model
from sb3_python2.policy import MlpPolicy, MultiInputPolicy

def recursive_getattr(obj, attr, *args):

    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split("."))

print("-------------load--------------")
env = gym.make(u"Pendulum-v0")
model = Model(env, MlpPolicy)
params = torch.load('model_torch.pth.tar')
for name in params:
    attr = None
    attr = recursive_getattr(model, name)
    attr.load_state_dict(params[name])

print("-------------test g change--------------")
env = gym.make("Pendulum-v0", g = 30.0)
print("gravity:{}".format(env.g))
sum_num = 0
reach_num = 0
for i in range(50):
    env.seed(2)
    obs = env.reset()

    reach = False
    for j in range(200):
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        if reach == False and rewards > -0.1:
            reach_num = j
            reach = True
        elif reach == True and rewards <= -0.1:
            reach = False
        # env.render()
    if reach == True:
        sum_num += reach_num
    else:
        sum_num += 199
print("sum steps in 50 tests to reach upright: {}".format(sum_num))
env.close()

print("-------------test g no change--------------")
env = gym.make("Pendulum-v0")
print("gravity:{}".format(env.g))
sum_num = 0
reach_num = 0
for i in range(50):
    env.seed(2)
    obs = env.reset()
    reach = False
    for j in range(200):
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        if reach == False and rewards > -0.1:
            reach_num = j
            reach = True
        elif reach == True and rewards <= -0.1:
            reach = False
        # env.render()
    if reach == True:
        sum_num += reach_num
    else:
        sum_num += 199
print("sum steps in 50 tests to reach upright: {}".format(sum_num))
env.close()