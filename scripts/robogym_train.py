import torch
from robogym.utils.env_utils import load_env
from stable_baselines3 import SAC

from Sim2Real_py3.sb3_wrapper import run

if __name__ == "__main__":
    """
    The main function to train a policy on the robogym environment
    BlockRearrangeEnv based on the sac algorithm and MultiInputPolicy
    in stable-baselines3.
    """

    print("-------------train--------------")

    # sb3 wrapper
    run()

    # train model from env
    names = "./Sim2Real_py3/robogym_wrapper.py"
    kwargs = {"parameters": {"simulation_params": {"num_objects": 1}}}
    sim_env, args_remaining = load_env(names, return_args_remaining=True,
                                       **kwargs)
    model = SAC("MultiInputPolicy", sim_env)
    # /off_policy_algorithm/_dump_logs
    model.learn(total_timesteps=10000, log_interval=10)

    # save model and delete
    torch.save(model.get_parameters(), "model_robogym_torch.pth.tar",
               _use_new_zipfile_serialization=False)
    del model
    sim_env.close()
