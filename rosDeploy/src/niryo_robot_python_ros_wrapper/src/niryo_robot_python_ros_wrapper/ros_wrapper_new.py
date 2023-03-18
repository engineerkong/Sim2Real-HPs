from niryo_robot_python_ros_wrapper.ros_wrapper import *
import numpy as np
from datetime import datetime
from gym.spaces import Box, MultiDiscrete, Dict

class NiryoRosWrapperNew(NiryoRosWrapper):

    def __init__(self, model, num_eval, num_episodes):
        super(NiryoRosWrapperNew, self).__init__()

        self.model = model
        self.num_eval = num_eval
        self.num_episodes = num_episodes
        
        # TODO: An example here to initial the observation to get the value of velocity.

        self.obs_prev = {
            "obj_pos": np.array([[0., 0., 0.]]),
            "obj_rel_pos": np.array([[0., 0., 0.]]),
            "obj_vel_pos": np.array([[0., 0., 0.]]),
            "obj_rot": np.array([[0., 0., 0.]]),
            "obj_vel_rot": np.array([[0., 0., 0.]]),
            "robot_joint_pos": np.array([0., 0., 0., 0., 0., 0.]),
            "gripper_pos": np.array([0., 0., 0.]),
            "gripper_velp": np.array([0., 0., 0.]),
            "gripper_controls": np.array([0.]),
            "gripper_qpos": np.array([0.]), 
            "gripper_vel": np.array([0.]),
            "qpos": np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]), 
            "qpos_goal": np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]), 
            "goal_obj_pos": np.array([[0., 0., 0.]]),
            "goal_obj_rot": np.array([[0., 0., 0.]]),
            "is_goal_achieved": np.array([0], dtype='int32'),
            "rel_goal_obj_pos": np.array([[0., 0., 0.]]),
            "rel_goal_obj_rot": np.array([[0., 0., 0.]]),
            "obj_gripper_contact": np.array([[0., 0.]]),
            "obj_bbox_size": np.array([[0., 0., 0.]]),
            "obj_colors": np.array([[0., 0., 0., 0.]]),
            "safety_stop": np.array([False]),
            "tcp_force": np.array([0., 0., 0.]),
            "tcp_torque": np.array([0., 0., 0.]),
            "action_ema": np.array([0., 0., 0., 0., 0., 0.])
        }
        workspace_name = "gazebo_1"
        if workspace_name in self.get_workspace_list():
            self.delete_workspace(workspace_name)

        workspace_pose = [0.25, 0.0, 0.001]
        point_1 = [workspace_pose[0] + 0.087, workspace_pose[1] + 0.087, workspace_pose[2]]
        point_2 = [workspace_pose[0] + 0.087, workspace_pose[1] - 0.087, workspace_pose[2]]
        point_3 = [workspace_pose[0] - 0.087, workspace_pose[1] - 0.087, workspace_pose[2]]
        point_4 = [workspace_pose[0] - 0.087, workspace_pose[1] + 0.087, workspace_pose[2]]

        self.save_workspace_from_points(workspace_name, [point_1, point_2, point_3, point_4])
        self.calibrate_auto()

        observation_pose = (0.18, 0., 0.35, 0., 1.57, -0.2)
        self.move_pose(*observation_pose)

    def eval(self):
        list_num_eval = np.zeros(self.num_episodes)
        list_reward = np.zeros(self.num_episodes)
        for i in range(self.num_eval):
            self.time1 = datetime.now()
            obs = self.get_observation()
            for j in range(self.num_episodes):
                print("episode:{}".format(j))
                action, _states = self.model.predict(obs)
                obs, reward = self.step(action)
                list_num_eval[j] = j
                list_reward[j] += reward
        list_reward /= self.num_eval

        return list_num_eval, list_reward

    def step(self, action):
        tcp_pose = self.get_pose()
        robot_pose = self.obs_prev['robot_joint_pos']
        # Change the movepose from relative to absolute.
        action_movepose = np.zeros_like(action)
        action_movepose[:3] = robot_pose[:3] + action[:3] - 5
        action_movepose[3] = robot_pose[3] + action[4] - 5
        action_movepose[4] = robot_pose[4] + 0.0
        action_movepose[5] = robot_pose[5] + action[3] - 5
        action_gripper = action[5] - 5
        
        # Move robot end effector pose to a (x, y, z, roll, pitch, yaw) absolute pose.
        movement = [tcp_pose.position.x, tcp_pose.position.y, tcp_pose.position.z,
                    tcp_pose.rpy.roll, tcp_pose.rpy.pitch, tcp_pose.rpy.yaw]
        # TODO: An example here, stay in the observation position.

        self.move_pose(movement[0], movement[1], movement[2], 
                       movement[3], movement[4], movement[5])
        if action_gripper > 0:
            self.close_gripper()
        elif action_gripper < 0:
            self.open_gripper()
        obs = self.get_observation()
        reward = self.get_reward(action)

        return obs, reward

    def get_observation(self):

        object_found, object_pose, object_shape, object_color = self.detect_object(
            "gazebo_1", shape = ObjectShape.ANY, color = ObjectColor.ANY)
        tcp_pose = self.get_pose()
        robot_joint = self.get_joints()
        goal_pose = self.get_target_pose_from_rel("gazebo_1", 0., 0., 0., 0.)
        target_pose = {"cube_blue":[0.25, 0.025, 0.011, 1.0, 1.0, 1.0], 
            "cube_red":[0.26, -0.05, 0.011, 1.0, 1.0, 0.5], 
            "cube_green":[0.2, -0.03, 0.011, 0.0, 1.0, 0.5]}
        

        self.time2 = datetime.now()
        delta_time = (self.time2 - self.time1).microseconds/1000000 # Todo: float
        self.time1 = self.time2

        # TODO: An example here, because not sure if object detected or not, use the following as observation firstly.

        obs = {'obj_pos': np.array([[1.45028845, 0.76641951, 0.51168497]]), 
               'obj_rel_pos': np.array([[ 0.02206645,  0.27219146, -0.10901402]]), 
               'obj_vel_pos': np.array([[ 0.26896318,  0.20836472, -0.30946774]]), 
               'obj_rot': np.array([[-5.65698990e-08,  4.52449500e-08,  1.64037413e+00]]), 
               'obj_vel_rot': np.array([[ 1.33117120e-05, -1.06467885e-05,  7.59863338e-22]]), 
               'robot_joint_pos': np.array([ 2.4699694 , -1.1105487 ,  2.22886699, -2.29691246, -4.22710327, 3.29787323]), 
               'gripper_pos': np.array([1.428222  , 0.49422805, 0.62069899]), 
               'gripper_velp': np.array([-0.26896345, -0.20836506,  0.31153658]), 
               'gripper_controls': np.array([-0.04015981]), 
               'gripper_qpos': np.array([-0.03641363]), 
               'gripper_vel': np.array([-0.0287117]), 
               'qpos': np.array([ 2.46996940e+00, -1.11054870e+00,  2.22886699e+00, -2.29691246e+00,
                -4.22710327e+00,  3.29787323e+00, -3.64082164e-02, -3.64136335e-02,
                1.45028845e+00,  7.66419512e-01,  5.11684974e-01,  6.82084423e-01,
                -2.74950836e-09,  3.61144700e-08,  7.31273437e-01]), 
                'qpos_goal': np.array([ 2.46543772, -1.1025591 ,  2.20527577, -2.27853246, -4.23384977,
                3.29448169, -0.0357493 , -0.0357492 ,  1.28460894,  0.5337104 , 0.51164   ,  0.68208442,  0.        ,  0.        ,  0.73127344]), 
                'goal_obj_pos': np.array([[1.28460894, 0.5337104 , 0.51164   ]]), 
                'goal_obj_rot': np.array([[-0.        ,  0.        ,  1.64037413]]), 
                'is_goal_achieved': np.array([0], dtype='int32'), 
                'rel_goal_obj_pos': np.array([[-1.65679512e-01, -2.32709116e-01, -4.49711422e-05]]), 
                'rel_goal_obj_rot': np.array([[ 5.65698990e-08, -4.52449500e-08,  2.22044605e-15]]), 
                'obj_gripper_contact': np.array([[0., 0.]]), 
                'obj_bbox_size': np.array([[0.0271044, 0.0271044, 0.0254   ]]), 
                'obj_colors': np.array([[0., 0., 1., 1.]]), 
                'safety_stop': np.array([False]), 
                'tcp_force': np.array([-2.20864904, -2.70963949, -5.22582722]), 
                'tcp_torque': np.array([-0.39828929,  0.27908455,  0.02438468]),
                "action_ema": np.array([0., 0., 0., 0., 0., 0.])}
        
        # obs = {"obj_pos": object_pose[:3],
        #     "obj_rel_pos": object_pose[:3] - tcp_pose[:3],
        #     "obj_vel_pos": ((object_pose[:3] - tcp_pose[:3]) - self.obs_prev["obj_rel_pos"])/delta_time,
        #     "obj_rot": object_pose[3:],
        #     "obj_vel_rot": (object_pose[3:] - self.obs_prev)/delta_time,
        #     "robot_joint_pos": robot_joint,
        #     "gripper_pos": tcp_pose[:3],
        #     "gripper_velp": (tcp_pose[:3] - self.obs_prev["gripper_pos"])/delta_time,
        #     "gripper_controls": np.array([0.]),
        #     "gripper_qpos": np.array([0.]), 
        #     "gripper_vel": (np.array([0.]) - self.obs_prev["gripper_qpos"])/delta_time,
        #     "qpos": np.array([ 2.66900897e+00, -1.34649713e+00,  2.51238354e+00, -2.33887284e+00,
        #             -4.12683264e+00,  1.09416889e+00, -3.57420643e-05, -3.56767674e-05,
        #             1.24755622e+00,  6.41423717e-01,  5.11673149e-01,  8.27861037e-01,
        #             0.00000000e+00,  0.00000000e+00,  5.60933244e-01]), 
        #     "qpos_goal": np.array([ 2.66900897e+00, -1.34649713e+00,  2.51238354e+00, -2.33887284e+00,
        #             -4.12683264e+00,  1.09416889e+00, -3.57420643e-05, -3.56767674e-05,
        #             1.24755622e+00,  5.68701217e-01,  5.11640000e-01,  8.27861037e-01,
        #             0.00000000e+00,  0.00000000e+00,  5.60933244e-01]), 
        #     "goal_obj_pos": goal_pose[:3],
        #     "goal_obj_rot": goal_pose[3:],
        #     "is_goal_achieved": np.array([0], dtype='int32'),
        #     "rel_goal_obj_pos": object_pose[:3] - goal_pose[:3],
        #     "rel_goal_obj_rot": object_pose[3:] - object_pose[3:],
        #     "obj_gripper_contact": np.array([[0., 0.]]),
        #     "obj_bbox_size": object_shape,
        #     "obj_colors": object_color,
        #     "safety_stop": np.array([False]),
        #     "tcp_force": np.array([ 0.1913251 , -0.22139868, -2.95124764]),
        #     "tcp_torque": np.array([-0.04945587, -0.02993955, -0.00096012])}

        self.obs_prev = obs

        return obs

    def get_reward(self, action):
        # Set an object correctly for 1 point should be considered.
        
        # TODO: An example here, because not sure if object detected or not, here just use reward_ctrl as the total reward.

        # object_found, object_pose, object_shape, object_color = self.detect_object(
        #     "gazebo_1", shape = ObjectShape.ANY, color = ObjectColor.ANY)
        # tcp_pose = self.get_pose()
        # goal_pose = self.get_target_pose_from_rel()
        # vec_1 = object_pose - tcp_pose
        # vec_2 = object_pose - goal_pose
        # reward_near = -np.linalg.norm(vec_1)
        # reward_dist = -np.linalg.norm(vec_2)
        reward_ctrl = -np.square(action).sum()
        # reward = [reward_near, reward_dist, reward_ctrl]

        return reward_ctrl

