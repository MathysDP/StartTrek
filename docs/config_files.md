# Config files

## Overview

Configs are YAML files passed to scripts with `--config`. The scripts expect specific keys and will raise errors if required keys are missing.

Recommended locations:
- Training configs: configs/train/
- Evaluation configs: configs/eval/

## Common section: env

All configs must define the environment block:

- name: Gymnasium environment id (example: "LunarLander-v3")
- continuous: set to false (the policies and scripts assume discrete actions)
- gravity: float
- enable_wind: boolean
- wind_power: float
- turbulence_power: float
- seed: integer

## Training config schema

Required top-level keys:
- env
- train
- network
- epsilon
- replay_buffer
- target_update
- gamma
- reward_clipping
- additional_rewards
- name

Details:
- train
  - episodes: total training episodes
  - max_steps: max steps per episode
  - learning_rate: Adam learning rate
- network
  - hidden_sizes: list of integers for MLP layers
- epsilon
  - start: initial epsilon
  - end: minimum epsilon
  - decay_steps: decay schedule steps
- replay_buffer
  - capacity: max transitions stored
  - batch_size: sample size per training step
- target_update
  - type: "hard" or "soft"
  - frequency: used when type is "hard"
  - tau: used when type is "soft"
  - Note: include both frequency and tau to keep the file simple.
- gamma: discount factor
- reward_clipping
  - enabled: boolean
  - min: float
  - max: float
- additional_rewards
  - enabled: boolean
  - step: float added each step
  - truncation: float added on truncation
- name: used for output file names

Outputs:
- outputs/logs/<name>_log.csv
- outputs/models/<name>_model.pth

### Training example

```yaml
env:
  name: "LunarLander-v3"
  continuous: false
  gravity: -10.0
  enable_wind: false
  wind_power: 15.0
  turbulence_power: 1.5
  seed: 42

train:
  episodes: 2200
  max_steps: 1000
  learning_rate: 0.001

network:
  hidden_sizes: [64, 128, 64]

epsilon:
  start: 1.0
  end: 0.05
  decay_steps: 60000

replay_buffer:
  capacity: 75000
  batch_size: 32

target_update:
  type: "hard"
  frequency: 20
  tau: 0.005

gamma: 0.99

reward_clipping:
  enabled: false
  min: -10.0
  max: 10.0

additional_rewards:
  enabled: true
  step: -0.2
  truncation: -200.0

name: "baseConfig"
```

## Evaluation config schema

Required top-level keys:
- env
- eval
- policy
- name

Details:
- eval
  - episodes: number of episodes per seed
- policy
  - type: "heuristic", "random", or "DQN"
  - hidden_sizes: required only for "DQN" and must match the training network
  - Note: extra keys are ignored by the current scripts.
- name: used to locate the model file and name outputs

Outputs:
- outputs/videos/<name>-episode-*.mp4
- outputs/logs/<name>_eval_log<seed>.csv (seed runs from env.seed to env.seed + 4)

### Evaluation example

```yaml
env:
  name: "LunarLander-v3"
  continuous: false
  gravity: -10.0
  enable_wind: false
  wind_power: 15.0
  turbulence_power: 1.5
  seed: 0

eval:
  episodes: 100

policy:
  type: "DQN"
  hidden_sizes: [64, 128, 64]

name: "baseConfig"
```

## Notes and tips

- Use the same `name` in train and eval to load the correct model file.
- If `policy.type` is "DQN", ensure `hidden_sizes` matches the trained model.
- Extra YAML keys are ignored unless the scripts read them.
