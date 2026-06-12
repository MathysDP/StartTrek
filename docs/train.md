# train.py

## Purpose

Trains a DQN agent on LunarLander using a YAML config passed via --config.

## Usage

```bash
  python -m scripts.train --config configs/train/baseConfig.yaml
```

## Imports and why

- gymnasium: create and step the environment
- torch, torch.nn, torch.optim: build and train the Q-network
- numpy, pandas: reproducible seeding and CSV logging
- random, deque: replay buffer sampling and storage
- exp: smooth epsilon decay schedule
- get_config: load config file
- DQN_network: model definition

## Config keys used

- env: name, continuous, gravity, enable_wind, wind_power, turbulence_power, seed
- replay_buffer: capacity, batch_size
- network: hidden_sizes
- train: learning_rate, episodes, max_steps
- epsilon: start, end, decay_steps
- gamma
- target_update: type (hard or soft), frequency or tau
- additional_rewards: enabled, step, truncation
- reward_clipping: enabled, min, max
- name

## Environment setup

- env = gym.make(...) uses render_mode="rgb_array" and the env settings from config.
- The action space is discrete (4 actions for LunarLander).
- Seeds are set for random, numpy, torch, and the env action space.

## Replay buffer

- Stores tuples: (state, action, reward, next_state, done).
- push(): append a transition.
- sample(batch_size): random.sample then:
  - stack state and next_state tensors
  - convert action to long, reward to float32, done to float32
- __len__(): buffer size, used to gate training until enough data exists.

## Networks

- policy_net: trained every step, in train() mode.
- target_net: copy of policy_net, in eval() mode for stable targets.
- optimizer: Adam on policy_net parameters.
- loss_fn: MSE between current Q and target Q.

## Action selection (epsilon-greedy)

- With probability epsilon: random action from env.action_space.sample().
- Otherwise: policy_net(state.unsqueeze(0)) and take argmax.
- torch.no_grad() avoids tracking gradients during action selection.

## Training step

- Skip if replay buffer has fewer items than batch_size.
- Compute current Q for taken actions using gather().
- Compute target Q using target_net and:
  target = reward + gamma * next_q * (1 - done)
- Backprop on MSE loss, then optimizer.step().
- Returns loss value for logging.

## Epsilon schedule

- epsilon = end + (start - end) * exp(-steps_done / decay_steps)
- Decays every environment step, not per episode.

## Training loop

For each episode:
1. Reset env with seed + episode.
2. Step loop up to train.max_steps:
   - Compute epsilon and select action.
   - Step env and get next_state, reward, terminated, truncated.
   - Optional extra rewards and reward clipping.
   - Store transition in replay buffer.
   - Run train_step and update state.
   - Track total_reward and steps.
   - If done, set termination cause and break.
3. Update target_net:
   - hard: copy every target_update.frequency episodes
   - soft: tau blending each episode
4. Append stats to data list.

## Outputs

- CSV log: outputs/logs/<name>_log.csv
- Model weights: outputs/models/<name>_model.pth

## Notes

- total_reward uses the raw reward (not the clipped reward).
- The script runs on import; use it as a script with --config.
