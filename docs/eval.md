# eval.py

## Purpose
Evaluates a policy on LunarLander, records per-episode statistics and saves videos.

## Usage
```bash
python -m scripts.eval --config configs/eval/<config_name>.yaml
```

## Imports
- gymnasium: environment creation
- RecordEpisodeStatistics: per-episode step and reward information
- RecordVideo: capture a video for every episode
- pandas: write CSV logs
- heuristic_policy, random_policy, DQN_policy: policy selection
- get_config: load the YAML configuration file

## Configuration keys
You can find some examples of configuration files in **configs/eval/**.
You can also create your own configuration file by following the [configuration files guide](config_files.md), more precisely, the part about evaluation configurations.

## Environment and wrappers
1. Create the environment using **gym.make()** with settings from **config["env"]**.
```python
env = gym.make(
	config["env"]["name"],
	render_mode="rgb_array",
	continuous=config["env"]["continuous"],
	gravity=config["env"]["gravity"],
	enable_wind=config["env"]["enable_wind"],
	wind_power=config["env"]["wind_power"],
	turbulence_power=config["env"]["turbulence_power"]
)
```

2. Wrap the environment with **RecordVideo()** to save videos of each episode, in **outputs/videos** with the naming pattern **<config_name>-episode-<episode>.mp4**.
```python
env = RecordVideo(
  env,
  video_folder="outputs/videos",
  name_prefix=config['name'],
  episode_trigger=lambda x: True
)
```
3. Wrap the environment with **RecordEpisodeStatistics()** to track episode rewards and steps.
```python
env = RecordEpisodeStatistics(env)
```

## Policy selection
Select the policy based on **config["policy"]["type"]**. There are four possibilities:
1. Random policy
```python
policy = random_policy()
```
2. Heuristic policy
```python
policy = heuristic_policy()
```
3. DQN policy
For DQN, the configuration must include **hidden_sizes** for the network architecture. The policy is initialized with the path to the saved model weights and the input/output sizes.
```python
policy = DQN_policy("outputs/models/" + config["name"] + "_model.pth", 8, 4, *config["policy"]["hidden_sizes"])
```
4. Unknown policy type
```python
raise ValueError(f"Unknown policy type: {config['policy']['type']}")
```

## Evaluation loop
For each seed in range **config["env"]["seed"]** to **config["env"]["seed"] + 4**:
1. Reset the environment with the current seed.
2. Process over **config["env"]["episodes"]** episodes and for each episode, run a step loop until termination or truncation:
    1. Initialize a step counter and a rewards accumulator.
    2. In the step loop:
        - Action is obtained from the policy by calling **policy(state, env)**.
        - Step the environment with **env.step(action)** to get the next state, reward, termination and truncation flags and additional info.
        - Update rewards according to potential clipping rules or additional logic.
        - Update the total reward and increment the step counter.
        - Determine the cause of termination based on the reward and final state (safe landing, crash, out of viewport, sleep, truncation).
    3. Save the episode's statistics (episode index, total rewards, steps, termination cause) to a list for logging.
3. After all episodes for the current seed are completed, save the collected statistics to a CSV file in **outputs/logs** with the naming pattern **<config_name>_eval_log<seed>.csv**.

## Outputs
The evaluation generates the following outputs:
- Videos: one video per episode saved in **outputs/videos** with the naming pattern **<config_name>_episode-<episode>.mp4**.
- CSV log: one CSV file in **outputs/logs/<name>_eval_log<seed>.csv** per seed.

## Notes
- Certain policies may require specific configurations, such as hidden layer sizes for DQN. Ensure that the configuration file is set up correctly for the chosen policy.
- The evaluation loop is designed to be flexible and can be extended with additional policies or environment settings as needed.
