from gym.envs.registration import register

register(id='Env2048-v1',
    entry_point='gym_2048.envs:Env2048',
    max_episode_steps = 3000
)

