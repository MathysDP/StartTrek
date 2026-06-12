# train.py

## Purpose
Trains a DQN agent on LunarLander using a YAML config passed via the **--config** argument.

## Usage
```bash
  python -m scripts.train --config configs/train/<config_name>.yaml
```

## Imports
- gymnasium: create and step the environment
- torch, torch.nn, torch.optim: build and train the Q-network
- numpy, pandas: reproducible seeding and CSV logging
- random, deque: replay buffer sampling and storage
- exp: smooth epsilon decay schedule
- get_config: load config file
- DQN_network: model definition

## Configuration keys
You can find some examples of configuration files in **configs/train/**.
You can also create your own configuration file by following the [configuration files guide](config_files.md), more precisely, the part about training configurations.

## Environment
1. Create the environment using **gym.make()** with settings from **config["env"]**.
```python
env = gym.make(
  config["env"]["name"],
  continuous=config["env"]["continuous"],
  gravity=config["env"]["gravity"],
  enable_wind=config["env"]["enable_wind"],
  wind_power=config["env"]["wind_power"],
  turbulence_power=config["env"]["turbulence_power"]
)
```

2. Set seeds for reproducibility. This includes the environment seed, as well as seeds for random, numpy and torch.

## Replay buffer
### Initialization
The buffer is initialized as an empty deque with a fixed maximum length, given by **config["replay_buffer"]["capacity"]**.

### Push method
The **push()** method takes a transition tuple (state, action, reward, next_state, done) and appends it to the buffer.
If the buffer exceeds its maximum capacity, the oldest transition is automatically removed due to the deque's behavior.

### Sample method
The **sample(batch_size)** method randomly samples a batch of transitions from the buffer.
It uses **random.sample()** to select a specified number of transitions.
The sampled transitions are then unpacked into separate tensors for states, actions, rewards, next_states and done flags, which are returned for use in training.

### Length method
The **__len__()** method returns the current number of transitions stored in the buffer, which is used to check if there are enough data to start training.

## Networks
Two networks are created:
- policy_net: the main Q-network that is trained every step, in train() mode.
- target_net: a copy of policy_net that is used in eval() mode for stable targets.

The target_net is updated less frequently than the policy_net, either by copying weights every few episodes (hard update) or by slowly blending weights every episode (soft update).

## Optimizer and loss function
The optimizer is Adam, applied to the parameters of the policy_net.

The loss function is Mean Squared Error (MSE) between the current Q-values and the target Q-values.
If the loss value is high, it may indicate that the agent is learning and updating its policy.
If the loss is low and stable, it may indicate convergence. However, if the loss is high and fluctuating, it may indicate instability in training.

## Action selection (epsilon-greedy)
The **select_action()** function follows an epsilon-greedy strategy.
If the random number is less than epsilon, a random action is selected from the environment's action space (**env.action_space.sample()**).
Otherwise, the action with the highest Q-value is selected from the policy_net for the current state (**policy_net(state.unsqueeze(0))**).

The epsilon value decays over time according to the schedule defined in the configuration, encouraging more exploration in the early stages of training and more exploitation as training progresses (see epsilon schedule).

The **torch.no_grad()** context is used during action selection to avoid tracking gradients.

## Training step
The **train_step()** function performs one optimization step on the policy_net using a batch of transitions from the replay buffer.
If the replay buffer has fewer items than the specified batch size, the function returns None and skips the training step to avoid errors from insufficient data.
Otherwise, it samples a batch of transitions and computes the loss as follows:
- Get a sample of transitions (state, action, reward, next_state, done) from the replay buffer.
- Compute current Q-values for the sampled states and actions using the policy_net.
- Compute next Q-values for the sampled next_states using the target_net and take the maximum Q-value across actions for each next_state.
- Compute target Q-values using the Bellman equation: **target = reward + gamma * next_q * (1 - done)**
- Backpropagate the loss (MSE between current Q and target Q) and perform an optimization step on the policy_net.
- Returns the loss value for logging purposes.

## Epsilon schedule


- epsilon = end + (start - end) * exp(-steps_done / decay_steps)
- Decays every environment step, not per episode.

## Training loop
At the start of training, the environment is reset to get the initial seed (**config["env"]["seed"]**).

For each episode in the range of **config["env"]["episodes"]**:
1. Initialization of episode statistics (total_reward, steps) and termination cause.
2. Process over steps until termination or truncation, or until reaching the maximum number of steps defined in the configuration (**config["train"]["max_steps"]**):
    - Update epsilon according to the schedule.
    - Select action using the epsilon-greedy strategy.
    - Step the environment with the selected action and observe the next state, reward, termination and truncation flags.
    - Optional: modify the reward (e.g., extra rewards for specific events, reward clipping).
    - Store the transition (state, action, modified reward, next_state, done) in the replay buffer.
    - Perform a training step on the policy_net using a batch of transitions from the replay buffer.
    - Update the current state to the next state and accumulate rewards and steps.
    - If the episode is terminated or truncated, determine the cause of termination (safe landing, crash, out of viewport, sleep, truncation) based on the reward and final state, and break the step loop.
3. After each episode, update the target_net according to the specified update strategy (hard or soft).
4. Append the episode's statistics (episode index, total rewards, steps, termination cause) to a list for logging.

## Outputs
- CSV log: a CSV file at **outputs/logs/<name>_log.csv** containing episode statistics (episode index, total rewards, steps, termination cause).
- Model: the model weights at **outputs/models/<name>_model.pth** saved after training is complete.

## Notes
- total_reward uses the modified reward (after optional extra rewards and clipping).
