import gymnasium as gym
from gymnasium.wrappers import RecordEpisodeStatistics, RecordVideo
from heuristic_policy import policy, PREFIX

SEED = 42
nb_episodes=5
env = gym.make("LunarLander-v3", render_mode="rgb_array")  # discrete by default
env = RecordVideo(
    env,
    video_folder="lunarlander-agent",    # Folder to save videos
    name_prefix=PREFIX,               # Prefix for video filenames
    episode_trigger=lambda x: True    # Record every episode
)

env = RecordEpisodeStatistics(env, buffer_length=nb_episodes)

obs, info = env.reset(seed=SEED)
i = 0
for episode in range(nb_episodes):
	obs, info = env.reset()
	episode_over = False
	reward = 0
	while not episode_over:
		if i == 1:
			print(obs)
		action = policy(obs, env)  # random or learned
		obs, r, terminated, truncated, info = env.step(action)
		reward += r
		if terminated or truncated:
			print(reward)
			episode_over = True
		i += 1

env.close()