# mygym_train


## Description
This branch trains and tests the policy on the sim environment mygym.


## Original Repo
```
https://github.com/incognite-lab/mygym.git
```


## Installation
```
# combine virtual environment with autorl-landscape3.8

git clone -b mygym_train git@github.com:automl-private/Sim2Real-HPs.git
cd Sim2Real-HPs

conda create -n mygym_train python=3.8
conda activate mygym_train

# Install for usage
python setup.py develop

# Install for development
make install-dev

# Install stable-baselines3 for the using of sac algorithm
pip install stable-baselines3[extra]==1.5.0

# Install hydra to configure
pip install hydra-core --upgrade

# Install wandb to visualize the training
pip install wandb

cd myGym

# Download pretrained visual modules
sh download_vision.sh

# Download pretrained baseline models
sh download_baselines.sh

# Check, whether the toolbox works
sh ./speed_checker.sh
```

## Minimal Example
```
cd myGym

# Train or test policy on mygym using config.yaml
python train_hydra.py
```
