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

mean = 0
best_episode = tuple()
for episode in range(nb_episodes):
	obs, info = env.reset(seed=SEED + episode)
	episode_over = False
	reward = 0
	while not episode_over:
		action = policy(obs, env)
		obs, r, terminated, truncated, info = env.step(action)
		reward += r
		if terminated or truncated:
			if best_episode == () or reward > best_episode[1]:
				best_episode = (episode, reward)
			print(f"Episode {episode} : reward {reward}")
			mean += reward
			episode_over = True

print("\nbest episode:", best_episode[0], float(best_episode[1]))
print("Mean reward:", mean / nb_episodes)
env.close()