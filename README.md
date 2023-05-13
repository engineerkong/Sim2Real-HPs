# ros_deploy


## Description
This branch deploys the trained policy on the real environment ned2 ros simulation.


## Original Repo
```
https://github.com/NiryoRobotics/ned_ros
```


## Installation
```
git clone -b ros_deploy git@github.com:automl-private/Sim2Real-HPs.git
cd Sim2Real-HPs

conda create -n ros_deploy python=2.7
conda activate ros_deploy

# Install for usage
pip install .

# Install for development
make install-dev

# Install ros dependencies 
caution:
ros-melodic is based on Ubuntu 18.04
ROS Python packages are only installed for the default system-provided Python interpreter 
the suitable python version for ned2 ros simulation is 2.7, it will be recommanded not use anaconda to control dependencies

# 1. follow ros melodic installation 
# http://wiki.ros.org/melodic/Installation/Ubuntu

# 2. follow install packages and catkin_make:
rosdep update
rosdep install --from-paths src --ignore-src --default-yes --rosdistro melodic --skip-keys "python-rpi.gpio"
cd Sim2Real_py2
catkin_make
echo "source $(pwd)/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc

# (optional, if use conda) using following if catpkg not found:
pip install -U rosdep rosinstall_generator wstool rosinstall six vcstools
unlink src/CMakeLists.txt
rm -rf build
rm -rf devel
rm .catkin_workspace
```


## Work points
```
1. a wrapper of deploying policy (niryo_robot_python_ros_wrapper/ros_wrapper_mygym)

2. a package of python2.7 version stable-baselines3 (especially sac) (niryo_robot_bringup/sb3_python2)

3. a detection improve code (niryo_robot_bringup/detection_improve)

4. a main code to deploy trained policy from mygym on ned2 ros simulation (niryo_robot_bringup/deploy)

5. a file contains trained policy from mygym (model_torch.pth.tar)
```


## Minimal Example
```
cd rosDeploy

# Simulation with physics
roslaunch niryo_robot_bringup desktop_gazebo_simulation.launch

# Deploy trained policy on simulation
rosrun niryo_robot_bringup deploy_reach.py
```
