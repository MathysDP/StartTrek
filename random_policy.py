import gymnasium as gym

PREFIX="random_policy"

def policy(obs, env):
    return env.action_space.sample()