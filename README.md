# Sim2Real_py3



## Installation
```
git clone https://github.com/automl/Sim2Real_py3.git
cd Sim2Real_py3
conda create -n Sim2Real_py3 python=3.7
conda activate Sim2Real_py3

# Install for usage
pip install .

# Install for development
make install-dev
```

## Minimal Example

```
# Firstly install robogym (which doesn't have pypi package)
pip install git+https://github.com/openai/robogym.git

# Sim2Real python3 is used to train policies by using stable-baselines3.

# Train a policy on Pendulum.
python ./scripts/pendulum_train.py

# Train a policy on Robogym/Rearrangeblock.
python ./scripts/robogym_train.py
```
