from gym.envs.registration import register

register(id='env2048-v1',
    entry_point='gym_2048.envs:env2048',
    max_episode_steps = 1000
)

