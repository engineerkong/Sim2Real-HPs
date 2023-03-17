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
        self.object_pose = np.zeros((18,))
        self.target_pose = np.array([0.2, -0.03, 0.011, 0.0, 1.0, 0.5])
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
            self.get_reward()
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
        ob_pose = np.array([self.pick_pose.position.x, self.pick_pose.position.y, self.pick_pose.position.z])
        ee_pose = np.array([self.tcp_pose.position.x, self.tcp_pose.position.y, self.tcp_pose.position.z])
        if np.linalg.norm(ee_pose - ob_pose) <= 0.05:
            self.close_gripper()
            self.gripper_object = 1
            self.pick_pose = self.tcp_pose
        elif np.linalg.norm(ee_pose[:2] - self.target_pose[:2]) <= 0.05 and self.gripper_object == 1:
            self.open_gripper()
            self.gripper_object = 0
            self.goal_achieve = 1
            self.pick_pose = self.target_pose

    def get_observation(self):
        # get the actual state
        object_found, object_pose, object_shape, object_color = self.detect_object(
            self.workspace, shape = ObjectShape.ANY, color = ObjectColor.ANY)
        if object_found:
            self.pick_pose = self.get_target_pose_from_rel(
                self.workspace, height_offset=0, x_rel=object_pose.x, y_rel=object_pose.y, yaw_rel=object_pose.yaw)
        if self.gripper_object == 1:
            touch = np.array([1], dtype='int32')
            self.pick_pose = self.tcp_pose
        else:
            touch = np.array([0], dtype='int32')
        # get the additional state
        self.tcp_pose = self.get_pose()
        # modify the euler to quaternion to suit the obs space
        obj_quat = quaternion_from_euler(self.pick_pose.rpy.roll, self.pick_pose.rpy.pitch, self.pick_pose.rpy.yaw)
        obj_6D = np.array([self.pick_pose.position.x, self.pick_pose.position.y, self.pick_pose.position.z, obj_quat[0], obj_quat[1], obj_quat[2], obj_quat[3]])
        goal_obj_quat = quaternion_from_euler(self.target_pose[3], self.target_pose[4], self.target_pose[5])
        goal_obj_6D = np.array([self.target_pose[0], self.target_pose[1], self.target_pose[2], goal_obj_quat[0], goal_obj_quat[1], goal_obj_quat[2], goal_obj_quat[3]])
        endeff_xyz = np.array([self.tcp_pose.position.x, self.tcp_pose.position.y, self.tcp_pose.position.z])
        # save obs and print
        self.obs = np.concatenate((obj_6D, goal_obj_6D, endeff_xyz, touch),axis=0)
        print("observation:{}".format(self.obs))

    def get_reward(self):
        # use pnp reward instead
        reward_ctrl = -np.square(self.action).sum()
        self.reward = reward_ctrl
