import warnings
from gym import spaces

from sb3_py2.utils import get_schedule_fn
from sb3_py2.on_policy_algorithm import OnPolicyAlgorithm

class PPO(OnPolicyAlgorithm):

    def __init__(
        self,
        policy,
        env,
        learning_rate = 3e-4,
        n_steps = 2048,
        batch_size = 64,
        n_epochs = 10,
        gamma = 0.99,
        gae_lambda = 0.95,
        clip_range = 0.2,
        clip_range_vf = None,
        ent_coef = 0.0,
        vf_coef = 0.5,
        max_grad_norm = 0.5,
        use_sde = False,
        sde_sample_freq = -1,
        target_kl = None,
        tensorboard_log = None,
        create_eval_env = False,
        policy_kwargs = None,
        verbose = 0,
        seed = None,
        device = "auto",
        _init_setup_model = True,
    ):
        super(PPO, self).__init__(
            policy,
            env,
            learning_rate=learning_rate,
            n_steps=n_steps,
            gamma=gamma,
            gae_lambda=gae_lambda,
            ent_coef=ent_coef,
            vf_coef=vf_coef,
            max_grad_norm=max_grad_norm,
            use_sde=use_sde,
            sde_sample_freq=sde_sample_freq,
            tensorboard_log=tensorboard_log,
            policy_kwargs=policy_kwargs,
            verbose=verbose,
            device=device,
            create_eval_env=create_eval_env,
            seed=seed,
            _init_setup_model=False,
            supported_action_spaces=(
                spaces.Box,
                spaces.Discrete,
                spaces.MultiDiscrete,
                spaces.MultiBinary,
            ),
        )
        assert (
            batch_size > 1
        ), "`batch_size` must be greater than 1. See https://github.com/DLR-RM/stable-baselines3/issues/440"

        if self.env is not None:
            buffer_size = self.env.num_envs * self.n_steps
            assert (
                buffer_size > 1
            ), "`n_steps * n_envs` must be greater than 1. Currently n_steps and n_envs"
            untruncated_batches = buffer_size // batch_size
            if buffer_size % batch_size > 0:
                warnings.warn("warning")
        self.batch_size = batch_size
        self.n_epochs = n_epochs
        self.clip_range = clip_range
        self.clip_range_vf = clip_range_vf
        self.target_kl = target_kl
        if _init_setup_model:
            self._setup_model()

    def _setup_model(self):
        super(PPO, self)._setup_model()
        self.clip_range = get_schedule_fn(self.clip_range)
        if self.clip_range_vf is not None:
            if isinstance(self.clip_range_vf, (float, int)):
                assert self.clip_range_vf > 0, "`clip_range_vf` must be positive, " "pass `None` to deactivate vf clipping"

            self.clip_range_vf = get_schedule_fn(self.clip_range_vf)
