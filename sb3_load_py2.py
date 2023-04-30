from __future__ import absolute_import
import gym
import torch
import functools
from sb3_py2.sac_algorithm import SAC
from sb3_py2.sac_policy import MlpPolicy

def recursive_getattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split(u"."))

print(u"-------------load--------------")
env = gym.make(u"Pendulum-v0")
model = SAC(MlpPolicy, env)
params = torch.load(u"model_torch_sac.pth.tar")
for name in params:
    attr = None
    attr = recursive_getattr(model, name)
    attr.load_state_dict(params[name])

print(u"-------------test--------------")
env = gym.make(u"Pendulum-v0")
obs = env.reset()
for j in xrange(10):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
env.close()

print(u"finished!!!")