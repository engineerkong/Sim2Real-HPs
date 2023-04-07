#!/usr/bin/env python

# Imports
from niryo_robot_python_ros_wrapper.ros_wrapper import *
import numpy as np
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class NiryoRosWrapperMygym(NiryoRosWrapper):

    def __init__(self, model, num_eval, num_episodes, distance_threshold):
        super(NiryoRosWrapperMygym, self).__init__()

        self.model = model
        self.num_eval = num_eval
        self.num_episodes = num_episodes
        self.distance_threshold = distance_threshold
        self.workspace = 'gazebo_1'
        self.object_xyz = np.zeros((3,))
        self.target_xyz = np.array([0.1, 0.3, 0.1])
        self.gripper_object = 0
        self.goal_achieve = 0

        self.create_wks_gazebo(self.workspace)
        obs_joints = [0, 0.4, -0.4, 0, -1.57, 0]
        self.move_joints(*obs_joints)
        self.open_gripper()
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
                print("successfully pick and place!!!")
                break

        return list_num_eval, list_reward

    def step(self):
        # move joints to the action joints
        self.move_joints(*self.action)
        # calculate the distance among 3 states and decide to move the gripper
        if np.linalg.norm(self.endeff_6d[:3] - self.object_xyz) <= self.distance_threshold:
            self.close_gripper()
            self.gripper_object = 1
        elif np.linalg.norm(self.endeff_6d[:3] - self.target_xyz) <= self.distance_threshold\
                        and self.gripper_object == 1:
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

        o1 = self.object_xyz
        o2 = self.target_xyz
        o3 = self.endeff_6d[:3]
        if self.gripper_object==1:
            print("reached")
            reward = self.calc_dist_diff(obj1_position=o1, obj2_position=o2)
        else:
            print("not reached")
            reward = self.calc_dist_diff(obj1_position=o1, obj2_position=o2, obj3_position=o3)
        return reward
    
    def calc_dist_diff(self, obj1_position, obj2_position, obj3_position=None):
        """
        Calculate change in the distances between 3 objects in previous and in current step. Normalize the change by the value of distance in previous step.

        Params:
            :param obj1_position: (list) Position of the first object (actual_state)
            :param obj2_position: (list) Position of the second object (goal_state)
            :param obj3_position: (list) Position of the third object (additional_obs)
        Returns:
            :return norm_diff: (float) Sum of normalized differences of distances between 3 objects in previsous and in current step
        """
        def calc_distance(obj1, obj2):
            dist = np.linalg.norm(np.asarray(obj1[:3]) - np.asarray(obj2[:3]))

        if self.prev_obj1_position is None and self.prev_obj2_position is None and self.prev_obj3_position is None:
            self.prev_obj1_position = obj1_position
            self.prev_obj2_position = obj2_position
            self.prev_obj3_position = obj3_position

        if obj3_position is None:
            prev_diff_12 = calc_distance(self.prev_obj1_position, self.prev_obj2_position)
            current_diff_12 = calc_distance(obj1_position, obj2_position)
            norm_diff = (prev_diff_12 - current_diff_12) / prev_diff_12
        else:
            prev_diff_12 = calc_distance(self.prev_obj1_position, self.prev_obj2_position)
            current_diff_12 = calc_distance(obj1_position, obj2_position)
            prev_diff_13 = calc_distance(self.prev_obj1_position, self.prev_obj3_position)
            current_diff_13 = calc_distance(obj1_position, obj3_position)
            norm_diff = (prev_diff_12 - current_diff_12) / prev_diff_12 + (prev_diff_13 - current_diff_13) / prev_diff_13

        self.prev_obj1_position = obj1_position
        self.prev_obj2_position = obj2_position
        self.prev_obj3_position = obj3_position

        return norm_diff