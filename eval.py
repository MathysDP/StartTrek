# Modules
import gymnasium as gym
from gymnasium.wrappers import RecordEpisodeStatistics, RecordVideo

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
for episode in range(config["eval"]["episodes"]):
	state, info = env.reset(seed=config["env"]["seed"] + episode)
	episode_over = False
	rewards = 0

	while not episode_over:
		action = policy(state, env)
		state, reward, terminated, truncated, info = env.step(action)
		rewards += reward
		if terminated or truncated:
			if best_episode == () or rewards > best_episode[1]:
				best_episode = (episode, rewards)
			print(f"Episode {episode}: rewards {rewards}")
			if reward == 100:
				print("End with a safe landing")
			elif reward == -100:
				if state[0] > 1.0:
					print("End cause of out of viewport")
				elif state[2] == 0.0 and state[3] == 0.0:
					print("End cause of sleep")
				else:
					print("End with a crash")
			elif truncated:
				print("End caused by truncation")
			print("Episode had {} steps\n".format(info["episode"]["l"]))
			mean += rewards
			successful_episodes += 1 if rewards >= 200 else 0
			episode_over = True

print("Best episode:", best_episode[0], float(best_episode[1]))
print("Mean reward:", mean / config["eval"]["episodes"])
print("Successful episodes:", successful_episodes)
env.close()
