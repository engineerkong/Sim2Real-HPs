import numpy as np
from robogym.envs.rearrange.blocks import BlockRearrangeEnv

class Robogym_Wrapper(BlockRearrangeEnv):

    def step(self, action):

        obs, reward, done, info = super(Robogym_Wrapper, self).step(action)
        reward = self.get_reward(action)
        # print(obs)

        return obs, reward, done, info

    def get_reward(self, action):

        robot_obs = self.mujoco_simulation.robot.observe()
        object_pose = self.mujoco_simulation.get_object_pos()
        tcp_pose = robot_obs.tcp_xyz()
        goal_pose = self._goal["obj_pos"].copy()
        vec_1 = object_pose - tcp_pose
        vec_2 = object_pose - goal_pose
        reward_near = -np.linalg.norm(vec_1)
        reward_dist = -np.linalg.norm(vec_2)
        reward_ctrl = -np.square(action).sum()
        reward = [reward_near, reward_dist, reward_ctrl]

        return reward

make_env = Robogym_Wrapper.build
