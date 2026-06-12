# eval.py

## Purpose

Evaluates a policy on LunarLander, records per-episode stats, and saves videos.

## Usage

```bash
python -m scripts.eval --config configs/eval/simpleEval.yaml
```

## Imports and why

- gymnasium: environment creation
- RecordEpisodeStatistics: per-episode step and reward info
- RecordVideo: capture a video for every episode
- pandas: write CSV logs
- heuristic_policy, random_policy, DQN_policy: policy selection
- get_config: load the YAML config

## Config keys used

- env: name, continuous, gravity, enable_wind, wind_power, turbulence_power, seed
- eval: episodes
- policy: type (heuristic | random | DQN), hidden_sizes (for DQN)
- name

## Environment and wrappers

- env = gym.make(..., render_mode="rgb_array", ...) uses config env settings.
- RecordVideo wraps env to save videos to outputs/videos.
  - name_prefix uses config["name"]
  - episode_trigger=lambda x: True records every episode
- RecordEpisodeStatistics wraps env, but steps are tracked manually in code.

## Policy selection

- heuristic: heuristic_policy()
- random: random_policy()
- DQN: DQN_policy("outputs/models/<name>_model.pth", 8, 4, *hidden_sizes)
- Otherwise: raise ValueError for unknown policy type.

## Evaluation loop

For each seed in range config["env"]["seed"] to config["env"]["seed"] + 4:
1. env.reset(seed=seed)
2. For each episode:
   - Step loop:
     - action = policy(state, env)
     - step env, accumulate rewards
     - done = terminated or truncated
     - on done, compute termination cause and break
   - env.reset() for the next episode (no per-episode seed)
3. Log data:
   - episode index
   - rewards (sum of rewards)
   - steps (manual counter)
   - termination_cause

## Outputs

- Videos: outputs/videos (one per episode)
- CSV log: outputs/logs/<name>_eval_log<seed>.csv (one per seed)

## Notes

- DQN policy loads weights from outputs/models/<name>_model.pth.
- Termination cause is derived from the last reward and final state (safe landing, crash, out of viewport, sleep, truncation).
- The script runs on import; use it as a script with --config.
