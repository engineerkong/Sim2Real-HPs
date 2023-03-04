import numpy as np
from robogym.envs.rearrange.blocks import BlockRearrangeEnv

class Robogym_Wrapper(BlockRearrangeEnv):
    """
    A Wrapper class based on the Robogym environment (BlockRearrangeEnv).

    Here we use BlockRearrangeEnv as our training environment. To accomplish different task, 
    our approach is to change the reward calculation to encourage the robot to complete the 
    task. Therefore, we modify the environment here by setting a wrapper on it.
    """

    def step(self, action):
        """
        Modify the step function in BlockRearrangeEnv to change get_reward function in it.
        """
        obs, reward, done, info = super(Robogym_Wrapper, self).step(action)
        reward = self.get_reward(action)

        return obs, reward, done, info

    def get_reward(self, action):
        """
        Modify the get_reward function in step function to change the reward calculation.
        """
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

        # print(f"reward:{-1*np.sum(reward)}")
        return reward

make_env = Robogym_Wrapper.build
