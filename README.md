# mygym_train


## Description
This branch trains the policy on the sim environment mygym.


## Original Repo
```
https://github.com/incognite-lab/mygym.git
```


## Installation
```
git clone -b mygym_train git@github.com:automl-private/Sim2Real-HPs.git
cd Sim2Real-HPs
conda create -n mygym_train python=3.7
conda activate mygym_train

# Install for usage
pip install .

# Install for development
make install-dev

cd Sim2Real_py3

# Install mygym
python setup.py develop

# Check, whether the toolbox works
sh ./speed_checker.sh
```


## Work points
```
1. a new kuka robot model file with 6 joints motors (envs/robots/kuka_magenetic_gripper_sdf/kong.urdf)
   and modify utils/helpers to link the new model file

2. a new config file to train pnp on kong.urdf (configs/train_pnp_kong.json)

3. modify train.py to use stable-baselines3 and save by pytorch, and also modify utils/callbacks.py to 
   solve comming error from this change

4. a trained policy from mygym (model_torch.pth.tar)
```


## Minimal Example
```
cd SimeReal_py3

# Train policy on mygym by using kong and pnp
python train.py --config ./configs/train_pnp_kong.json
```
