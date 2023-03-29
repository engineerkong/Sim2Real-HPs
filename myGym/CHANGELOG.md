origin:
https://github.com/incognite-lab/myGym

change 0 (17.March):
    train.py - import stable_baselines3 instead of stable_baseline
             - import torch and use torch.save to store trained policy
    utils/callbacks.py - evaluate_policy() comment lines to avoid error from stable_baselines3

change 1 (31.March):
    configs/train_pnp_kong.py - configuration
    envs/robots/niryo_robot_description - the model package of ned2
    envs/base_env.py - render() change the view-matrix compute methode to rpy methode and use both camera_id, camera_6d as options
    envs/robot.py - init() move robot firstly to obs_joints  
                  - _set_motors() find camera_link
                  - get_joints_limits() use limit from urdf for joints
                  - get_cam_position()/get_cam_orientation() get the pos and ori of camera
    transform_function.py - import euler from quaternion
    envs/task.py - import import euler_from_quaternion
                 - reset_task() correct the spell error "border"
                 - render_images() add a new view-matrix compute methode with camera_6d
                 - get_additional_obs() add a key to make vision module can read goal obs
                 - get_observation() calculate posrpy and add a key
                 - check_obs_template() pass to avoid error
    envs/vision_module.py - import load yolact_vision
                          - init() add observation to read goal obs
                          - get_module_type_key() edit get_module_type to read goal obs
                          - get_obj_position() apply get_module_type_key to read goal obs
    utils/helpers.py - give the path of ned2 urdf to "kong"
    yolact_vision - load yolact_vision for camera detection
                  - modify new_config_dict

