import gymnasium as gym
from gymnasium.wrappers import RecordEpisodeStatistics, RecordVideo
from heuristic_policy import policy, PREFIX

SEED = 42
nb_episodes=50
env = gym.make("LunarLander-v3", render_mode="rgb_array")
env = RecordVideo(
    env,
    video_folder="lunarlander-agent",
    name_prefix=PREFIX,
    episode_trigger=lambda x: True
)

env = RecordEpisodeStatistics(env, buffer_length=nb_episodes)

i = 0
mean = 0
for episode in range(nb_episodes):
	obs, info = env.reset(seed=SEED + episode)
	episode_over = False
	reward = 0
	while not episode_over:
		if i == 1:
			print(obs)
		action = policy(obs, env)
		obs, r, terminated, truncated, info = env.step(action)
		reward += r
		if terminated or truncated:
			print(f"Episode {episode} : reward {reward}", episode)
			mean += reward
			episode_over = True
		i += 1

print("Mean reward:", mean / nb_episodes)
env.close()