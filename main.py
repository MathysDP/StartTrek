import gymnasium as gym
from gymnasium.wrappers import RecordEpisodeStatistics, RecordVideo
import heuristic_policy
import random_policy

SEED = 42
nb_episodes=50

user_input = None

while user_input not in ["heuristic", "random"]:
	user_input = input("Choose a policy (heuristic/random): ").strip().lower()
	if user_input == "heuristic":
		policy = heuristic_policy.policy
		prefix = heuristic_policy.PREFIX
	elif user_input == "random":
		policy = random_policy.policy
		prefix = random_policy.PREFIX
	else:
		print("Invalid input. Please choose 'heuristic' or 'random'.")

env = gym.make("LunarLander-v3", render_mode="rgb_array", enable_wind=True, wind_power=15.0, turbulence_power=1.5)
env = RecordVideo(
    env,
    video_folder="lunarlander-agent",
	name_prefix=prefix,
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
			print("Episode had {} steps\n".format(info["episode"]["l"]))
			mean += rewards
			episode_over = True

print("Best episode:", best_episode[0], float(best_episode[1]))
print("Mean reward:", mean / nb_episodes)
env.close()
