import numpy as np
from robogym.envs.rearrange.blocks import BlockRearrangeEnv


class Robogym_Wrapper(BlockRearrangeEnv):
    """
    A Wrapper class based on the Robogym environment (BlockRearrangeEnv).

    Here we use BlockRearrangeEnv as our training environment. To accomplish
    different task, our approach is to change the reward calculation to
    encourage the robot to complete the task. Therefore, we modify the
    environment here by setting a wrapper on it.
    """
    def _observe_simple(self):
        """
        To show the observation, modify the RearrangeEnv._observe_simple() function
        of default observation for the environment.
        """
        robot_obs = self.mujoco_simulation.robot.observe()

        obs = {
            "obj_pos": self.mujoco_simulation.get_object_pos(),
            "obj_rel_pos": self.mujoco_simulation.get_object_rel_pos(),
            "obj_vel_pos": self.mujoco_simulation.get_object_vel_pos(),
            "obj_rot": self.mujoco_simulation.get_object_rot(),
            "obj_vel_rot": self.mujoco_simulation.get_object_vel_rot(),
            "robot_joint_pos": robot_obs.joint_positions(),
            "gripper_pos": robot_obs.tcp_xyz(),
            "gripper_velp": robot_obs.tcp_vel(),
            "gripper_controls": robot_obs.gripper_controls(),
            "gripper_qpos": robot_obs.gripper_qpos(),
            "gripper_vel": robot_obs.gripper_vel(),
            "qpos": self.mujoco_simulation.qpos,
            "qpos_goal": self._goal["qpos_goal"].copy(),
            "goal_obj_pos": self._goal["obj_pos"].copy(),
            "goal_obj_rot": self._goal["obj_rot"].copy(),
            "is_goal_achieved": np.array([self._is_goal_achieved], np.int32),
            "rel_goal_obj_pos": self._goal_info_dict["rel_goal_obj_pos"].copy(),
            "rel_goal_obj_rot": self._goal_info_dict["rel_goal_obj_rot"].copy(),
            "obj_gripper_contact":
            self.mujoco_simulation.get_object_gripper_contact(),
            "obj_bbox_size":
            self.mujoco_simulation.get_object_bounding_box_sizes(),
            "obj_colors": self.mujoco_simulation.get_object_colors(),
            "safety_stop": np.array([robot_obs.is_in_safety_stop()]),
            "tcp_force": robot_obs.tcp_force(),
            "tcp_torque": robot_obs.tcp_torque(),
        }

        if self.constants.mask_obs_outside_placement_area:
            obs = self._mask_goal_observation
            (obs, self._goal["goal_objects_in_placement_area"].copy())
            obs = self._mask_object_observation(obs)

        return obs

    def step(self, action):
        """
        Modify the step function in BlockRearrangeEnv to change get_reward
        function in it.
        """
        obs, reward, done, info = super(Robogym_Wrapper, self).step(action)
        reward = self.get_reward(action)

        return obs, reward, done, info

    def get_reward(self, action):
        """
        Modify the get_reward function in step function to change the reward
        calculation.
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
