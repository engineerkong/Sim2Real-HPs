#!/usr/bin/env python

# Imports
from niryo_robot_python_ros_wrapper.ros_wrapper import *
import numpy as np
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class NiryoRosWrapperMygym(NiryoRosWrapper):

    def __init__(self, model, num_eval, num_episodes):
        super(NiryoRosWrapperMygym, self).__init__()

        self.model = model
        self.num_eval = num_eval
        self.num_episodes = num_episodes
        self.workspace = 'gazebo_1'
        self.object_xyz = np.zeros((3,))
        self.target_xyz = np.array([0.2, -0.03, 0.011])
        self.gripper_object = 0
        self.goal_achieve = 0

        self.create_wks_gazebo(self.workspace)
        obs_joints = [0, 0.4, -0.4, 0, -1.57, 0]
        self.move_joints(*obs_joints)
        self.get_observation()

    def create_wks_gazebo(self, workspace_name):
        workspace_name = workspace_name
        if workspace_name in self.get_workspace_list():
            self.delete_workspace(workspace_name)

        workspace_pose = [0.25, 0.0, 0.001]
        point_1 = [workspace_pose[0] + 0.087, workspace_pose[1] + 0.087, workspace_pose[2]]
        point_2 = [workspace_pose[0] + 0.087, workspace_pose[1] - 0.087, workspace_pose[2]]
        point_3 = [workspace_pose[0] - 0.087, workspace_pose[1] - 0.087, workspace_pose[2]]
        point_4 = [workspace_pose[0] - 0.087, workspace_pose[1] + 0.087, workspace_pose[2]]

        self.save_workspace_from_points(workspace_name, [point_1, point_2, point_3, point_4])

    def eval(self):
        # single evaluation
        list_num_eval = np.zeros(self.num_episodes)
        list_reward = np.zeros(self.num_episodes)
        for j in range(self.num_episodes):
            print("episode:{}".format(j))
            self.action, self._states = self.model.predict(self.obs)
            print("action:{}".format(self.action))
            self.step()
            self.get_observation()
            print("observation:{}".format(self.obs))
            self.get_reward()
            print("reward:{}".format(self.reward))
            list_num_eval[j] = j
            list_reward[j] += self.reward
            if self.goal_achieve == 1:
                print("success pick and place!!!")
                break

        return list_num_eval, list_reward

    def step(self):
        # move joints to the action joints
        self.move_joints(*self.action)
        # calculate the distance among 3 states and decide to move the gripper
        if np.linalg.norm(self.endeff_6d[:3] - self.object_xyz) <= 0.05:
            self.close_gripper()
            self.gripper_object = 1
        elif np.linalg.norm(self.endeff_6d[:3] - self.target_xyz) <= 0.05 and self.gripper_object == 1:
            self.open_gripper()
            self.gripper_object = 0
            self.goal_achieve = 1

    def get_observation(self):
        # get the actual state
        object_found, object_pose, object_shape, object_color = self.detect_object(
            self.workspace, shape = ObjectShape.ANY, color = ObjectColor.ANY)
        if object_found:
            self.object_xyz = np.array([object_pose.x, object_pose.y, object_pose.z])
        # get the additional state
        tcp_pose = self.get_pose()
        self.endeff_6d = np.array([tcp_pose.position.x, tcp_pose.position.y, tcp_pose.position.z, 
                                   tcp_pose.orientation.x, tcp_pose.orientation.y, tcp_pose.orientation.z, tcp_pose.orientation.w])
        if self.gripper_object == 1:
            self.object_xyz = self.endeff_6d[:3]
        # save obs and print
        self.obs = np.concatenate((self.object_xyz, self.target_xyz, self.endeff_6d),axis=0)

    def get_reward(self):
        # use pnp reward instead
        reward_ctrl = -np.square(self.action).sum()
        self.reward = reward_ctrl
