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
	rewards = 0
	while not episode_over:
		action = policy(obs, env)
		obs, reward, terminated, truncated, info = env.step(action)
		rewards += reward
		if terminated or truncated:
			if best_episode == () or rewards > best_episode[1]:
				best_episode = (episode, rewards)
			print(f"Episode {episode}: rewards {rewards}")
			if reward == 100:
				print("End with a safe landing")
			elif reward == -100:
				if obs[0] > 1.0:
					print("End cause of out of viewport")
				elif obs[2] == 0.0 and obs[3] == 0.0:
					print("End cause of sleep")
				else:
					print("End with a crash")
			mean += rewards
			episode_over = True

print("\nBest episode:", best_episode[0], float(best_episode[1]))
print("Mean reward:", mean / nb_episodes)
env.close()
