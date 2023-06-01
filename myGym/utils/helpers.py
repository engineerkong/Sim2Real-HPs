import numpy as np

def get_workspace_dict():
    ws_dict = {'table':    {'urdf': 'table.urdf', 'texture': 'table.jpg',
                                            'transform': {'position':[-0.0, -0.0, -1.05], 'orientation':[0.0, 0.0, 0*np.pi]},
                                            'robot': {'position': [0.0, 0.0, 0.0], 'orientation': [0.0, 0.0, 0.5*np.pi]},
                                            'camera': {'position': [[0.0, 2.4, 1.0], [-0.0, -1.5, 1.0], [1.8, 0.9, 1.0], [-1.8, 0.9, 1.0], [0., 0.85, 1.4],
                                                                    [0.0, 1.6, 0.8], [-0.0, -0.5, 0.8], [0.8, 0.9, 0.6], [-0.8, 0.9, 0.8], [0.0, 0.9, 1.]],
                                                        'target': [[0.0, 2.1, 0.9], [-0.0, -0.8, 0.9], [1.4, 0.9, 0.88], [-1.4, 0.9, 0.88], [0.0, 0.80, 1.],
                                                                   [0.0, 1.3, 0.5], [-0.0, -0.0, 0.6], [0.6, 0.9, 0.4], [-0.6, 0.9, 0.5], [0.0, 0.898, 0.8]]},
                                            'borders':[-0.7, 0.7, 0.5, 1.3, 0.1, 0.1]},
                                'workspace':    {'urdf': 'workspace.urdf', 'texture': 'table.jpg',
                                            'transform': {'position':[-0.0, 0.25, -0.0005], 'orientation':[0.0, 0.0, 0*np.pi]},
                                            'robot': {'position': [0.0, 0.0, 0.0], 'orientation': [0.0, 0.0, 0.5*np.pi]},
                                            'camera': {'position': [[0.0, 2.4, 1.0], [-0.0, -1.5, 1.0], [1.8, 0.9, 1.0], [-1.8, 0.9, 1.0], [0., 0.85, 1.4],
                                                                    [0.0, 1.6, 0.8], [-0.0, -0.5, 0.8], [0.8, 0.9, 0.6], [-0.8, 0.9, 0.8], [0.0, 0.9, 1.]],
                                                        'target': [[0.0, 2.1, 0.9], [-0.0, -0.8, 0.9], [1.4, 0.9, 0.88], [-1.4, 0.9, 0.88], [0.0, 0.80, 1.],
                                                                   [0.0, 1.3, 0.5], [-0.0, -0.0, 0.6], [0.6, 0.9, 0.4], [-0.6, 0.9, 0.5], [0.0, 0.898, 0.8]]},
                                            'borders':[-0.7, 0.7, 0.5, 1.3, 0.1, 0.1]}
                                            }
    return ws_dict


def get_robot_dict():
    r_dict =   {'ned2_camera': {'path': '/envs/robots/urdf/niryo_ned2_camera.urdf', 'position': np.array([0.0, 0.0, 0.003]), 'orientation': [0.0, 0.0, 0*np.pi]},
                             'ned2_gripper_camera': {'path': '/envs/robots/urdf/niryo_ned2_gripper1_n_camera.urdf', 'position': np.array([0.0, 0.0, 0.003]), 'orientation': [0.0, 0.0, 0*np.pi]}
                            }
    return r_dict
