from pyniryo import *
import numpy as np

class Ned2_Wrapper:

    def __init__(self, adress, model, num_eval, num_episodes):
        self.model = model
        self.num_eval = num_eval
        self.num_episodes = num_episodes
        ned = NiryoRobot(adress)
        ned.calibrate_auto()

    def eval(self):
        list_num_eval = np.zero(self.num_episodes)
        list_reward = np.zero(self.num_episodes)
        for i in self.num_eval:
            obs = self.get_observation()
            for j in range(num_episodes):
                action, _states = self.model.predict(obs)
                obs, reward = self.step(action)
                list_num_eval[j] = j
                list_reward[j] += reward
        list_reward /= self.num_eval

        return list_num_eval, list_reward

    def step(self, action):
        tcp_pose = ned.get_pose()
        # relative to absolute
        action_movepose = np.zeros_like(action)
        action_movepose[:3] = tcp_pose[:3] + action[:3] - 5
        action_movepose[3] = tcp_pose[3] + action[4] - 5
        action_movepose[4] = tcp_pose[4] + 0.0
        action_movepose[5] = tcp_pose[5] + action[3] - 5
        action_gripper = action[5] - 5

        print(a for i in action_movepose)
        print(action_gripper)
        ned.move_pose(a for i in action_movepose)
        if action_gripper > 0:
            ned.grasp_gripper()
        elif action_gripper < 0:
            ned.release_gripper()
        obs = self.get_observation()
        reward = self.get_reward(action)

        return obs, reward

    def get_observation(self):

        object_found, object_pose, object_shape, object_color = ned.detect_object()
        tcp_pose = ned.get_pose()
        robot_joint = ned.get_joint()
        goal_pose = ned.get_target_pose_from_rel()
        # Todo
        delta_time = time
        obs = {
            "obj_pos": object_pose[:3],
            "obj_rel_pos": object_pose[:3] - tcp_pose[:3],
            "obj_vel_pos": (object_pose[:3] - tcp_pose[:3])/delta_time,
            "obj_rot": object_pose[3:],
            "obj_vel_rot": object_pose[3:] - tcp_pose[3:],
            "robot_joint_pos": robot_joint,
            "gripper_pos": tcp_pose[:3],
            "gripper_velp": tcp_pose/delta_time,
            "gripper_controls": ned.pose2joint(tcp_pose),
            "gripper_qpos": ned.pose2joint(tcp_pose),
            "gripper_vel": ned.pose2joint(tcp_pose)/delta_time,
            "qpos": [tcp_pose, object_pose],
            "qpos_goal": [tcp_pose, goal_pose],
            "goal_obj_pos": goal_pose[:3],
            "goal_obj_rot": goal_pose[3:],
            "is_goal_achieved": check,
            "rel_goal_obj_pos": object_pose[:3] - goal_pose[:3],
            "rel_goal_obj_rot": object_pose[3:] - object_pose[3:],
            "obj_gripper_contact": check,
            "obj_bbox_size": object_shape,
            "obj_colors": object_color,
            "safety_stop": check,
            "tcp_force": check,
            "tcp_torque":check,
        }

        return obs

    def get_reward(self, action):

        object_found, object_pose, object_shape, object_color = ned.detect_object()
        tcp_pose = ned.get_pose()
        goal_pose = ned.get_target_pose_from_rel()
        vec_1 = object_pose - tcp_pose
        vec_2 = object_pose - goal_pose
        reward_near = -np.linalg.norm(vec_1)
        reward_dist = -np.linalg.norm(vec_2)
        reward_ctrl = -np.square(action).sum()
        reward = [reward_near, reward_dist, reward_ctrl]

        return reward

