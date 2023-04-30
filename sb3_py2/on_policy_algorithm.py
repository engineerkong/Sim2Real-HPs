from __future__ import absolute_import
import gym

from sb3_py2.buffers import DictRolloutBuffer, RolloutBuffer
from sb3_py2.base_policies import ActorCriticPolicy
from sb3_py2.base_algorithm import BaseAlgorithm

class OnPolicyAlgorithm(BaseAlgorithm):

    def __init__(
        self,
        policy,
        env,
        learning_rate,
        n_steps,
        gamma,
        gae_lambda,
        ent_coef,
        vf_coef,
        max_grad_norm,
        use_sde,
        sde_sample_freq,
        policy_base = ActorCriticPolicy,
        tensorboard_log = None,
        create_eval_env = False,
        monitor_wrapper = True,
        policy_kwargs = None,
        verbose = 0,
        seed = None,
        device = u"auto",
        _init_setup_model = True,
        supported_action_spaces = None,
    ):

        super(OnPolicyAlgorithm, self).__init__(
            policy=policy,
            env=env,
            policy_base=policy_base,
            learning_rate=learning_rate,
            policy_kwargs=policy_kwargs,
            verbose=verbose,
            device=device,
            use_sde=use_sde,
            sde_sample_freq=sde_sample_freq,
            create_eval_env=create_eval_env,
            support_multi_env=True,
            seed=seed,
            tensorboard_log=tensorboard_log,
            supported_action_spaces=supported_action_spaces,
        )
        self.n_steps = n_steps
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.ent_coef = ent_coef
        self.vf_coef = vf_coef
        self.max_grad_norm = max_grad_norm
        self.rollout_buffer = None
        if _init_setup_model:
            self._setup_model()

    def _setup_model(self):
        self._setup_lr_schedule()
        self.set_random_seed(self.seed)
        buffer_cls = DictRolloutBuffer if isinstance(self.observation_space, gym.spaces.Dict) else RolloutBuffer
        self.rollout_buffer = buffer_cls(
            self.n_steps,
            self.observation_space,
            self.action_space,
            self.device,
            gamma=self.gamma,
            gae_lambda=self.gae_lambda,
            n_envs=self.n_envs,
        )
        self.policy = self.policy_class(
            self.observation_space,
            self.action_space,
            self.lr_schedule,
            use_sde=self.use_sde,
            **self.policy_kwargs
        )
        self.policy = self.policy.to(self.device)