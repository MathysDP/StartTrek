# Modules
import gymnasium as gym
from gymnasium.wrappers import RecordEpisodeStatistics, RecordVideo
import pandas as pd

# Policies
from heuristic_policy import heuristic_policy
from random_policy import random_policy
from DQN_policy import DQN_policy

# Utils
from get_config import get_config

config = get_config()

env = gym.make(
	config["env"]["name"],
	render_mode="rgb_array",
	continuous=config["env"]["continuous"],
	gravity=config["env"]["gravity"],
	enable_wind=config["env"]["enable_wind"],
	wind_power=config["env"]["wind_power"],
	turbulence_power=config["env"]["turbulence_power"]
)

env = RecordVideo(
    env,
    video_folder=config["policy"]["video_folder"],
	name_prefix=config["policy"]["video_prefix"],
    episode_trigger=lambda x: True
)

env = RecordEpisodeStatistics(env, buffer_length=config["eval"]["episodes"])

if config["policy"]["type"] == "heuristic":
	policy = heuristic_policy()
elif config["policy"]["type"] == "random":
	policy = random_policy()
elif config["policy"]["type"] == "DQN":
	policy = DQN_policy(config["policy"]["save_path"], 8, 4, *config["policy"]["hidden_sizes"])
else:
	raise ValueError(f"Unknown policy type: {config['policy']['type']}")

mean = 0
best_episode = tuple()
successful_episodes = 0

data = []

for episode in range(config["eval"]["episodes"]):
	print(f"Episode {episode + 1} is running...")
	state, info = env.reset(seed=config["env"]["seed"] + episode)
	episode_over = False
	rewards = 0
	cause_of_termination = "unknown"

	while True:
		action = policy(state, env)
		state, reward, terminated, truncated, info = env.step(action)
		rewards += reward
		done = terminated or truncated

		if done:
			if reward == 100:
				cause_of_termination = "safe landing"
			elif reward == -100:
				if state[0] > 1.0:
					cause_of_termination = "out of viewport"
				elif state[2] == 0.0 and state[3] == 0.0:
					cause_of_termination = "sleep"
				else:
					cause_of_termination = "crash"
			elif truncated:
				cause_of_termination = "truncation"
			break

	data.append({
		"episode": episode,
		"rewards": rewards,
		"steps": info["episode"]["l"],
		"termination_cause": cause_of_termination
	})

env.close()

pd.DataFrame(data).to_csv(config["log_path"], index=False)

