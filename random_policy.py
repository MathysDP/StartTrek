class random_policy:
    def __init__(self):
        pass

    def __call__(self, state, env):
        return env.action_space.sample()
