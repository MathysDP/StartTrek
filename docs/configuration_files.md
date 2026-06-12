# Configuration files

## Overview
Configuration files are YAML files passed to scripts with **--config** argument.
There are two main types of configuration files:
- Training configs: used for training the DQN agent, containing all necessary hyperparameters and environment settings.
- Evaluation configs: used for evaluating a trained model, specifying evaluation parameters and policy type.

We recommend organizing these files in separate folders:
- Training configs: **configs/train/**
- Evaluation configs: **configs/eval/**

## Environment configuration (common to both training and evaluation)
All configurations must define the environment block:
- **name** (string): environment name, e.g. "LunarLander-v3"
- **continuous** (boolean): set to false (the policies and scripts assume discrete actions)
- **gravity** (float): gravitational acceleration
- **enable_wind** (boolean): whether to enable wind
- **wind_power** (float): wind power
- **turbulence_power** (float): turbulence power
- **seed** (integer): random seed for reproducibility

## Training configuration schema
### Required keys and details
- **env**: environment configuration (see above)
- **train**:
  - **episodes** (integer): total training episodes
  - **max_steps** (integer): max steps per episode
  - **learning_rate** (float): Adam learning rate
- **network**:
  - **hidden_sizes** (list of integers): sizes of MLP hidden layers
- **epsilon**:
  - **start** (float): initial epsilon value
  - **end** (float): minimum epsilon value
  - **decay_steps** (integer): number of steps over which epsilon decays
- **replay_buffer**:
  - **capacity** (integer): maximum number of transitions stored
  - **batch_size** (integer): number of transitions sampled per training step
- **target_update**:
  - **type** (string): "hard" or "soft"
  - **frequency** (integer): used when type is "hard", number of episodes between target network updates
  - **tau** (float): used when type is "soft", interpolation factor for soft updates
- **gamma** (float): discount factor for future rewards
- **reward_clipping**:
  - **enabled** (boolean): whether to clip rewards
  - **min** (float): minimum reward value when clipping is enabled
  - **max** (float): maximum reward value when clipping is enabled
- **additional_rewards**:
  - **enabled** (boolean): whether to add additional rewards
  - **step** (float): reward added at each step when enabled
  - **truncation** (float): reward added on episode truncation when enabled
- **name** (string): name used for output file naming

### Example
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

## Evaluation configuration schema
### Required keys and details
- **env**: environment configuration (see above)
- **eval**:
  - **episodes** (integer): number of episodes to evaluate per seed
- **policy**:
  - **type** (string): "heuristic", "random", or "DQN"
  - **hidden_sizes** (list of integers): required only for "DQN" and must match the training network architecture
- **name** (string): used to locate the model file and name outputs

### Example
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

## Notes
- Use the same **name** in train and evaluation configuration file to load the correct model file.
- If **policy.type** is "DQN", ensure **hidden_sizes** matches the trained model.
- Extra YAML keys are ignored unless the scripts read them.
