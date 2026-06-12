# Modules
import gymnasium as gym
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd

# Utils
import random
from collections import deque
from math import exp
from get_config import get_config

# Network
from DQN_policy import DQN_network

config = get_config()

env = gym.make(
    config["env"]["name"],
    render_mode="rgb_array",
    continuous=config["env"]["continuous"],
    gravity=config["env"]["gravity"],
    enable_wind=config["env"]["enable_wind"],
    wind_power=config["env"]["wind_power"],
    turbulence_power=config["env"]["turbulence_power"]
)

seed = config["env"]["seed"]
random.seed(seed)
np.random.seed(seed)
env.action_space.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

class ReplayBuffer:
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = zip(*batch)

        state = torch.stack(state)
        next_state = torch.stack(next_state)

        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float32)
        done = torch.tensor(done, dtype=torch.float32)

        return state, action, reward, next_state, done

    def __len__(self):
        return len(self.buffer)


replay_buffer = ReplayBuffer(config["replay_buffer"]["capacity"])

policy_net = DQN_network(8, 4, *config["network"]["hidden_sizes"])
policy_net.train()

target_net = DQN_network(8, 4, *config["network"]["hidden_sizes"])
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr=config["train"]["learning_rate"])
loss_fn = nn.MSELoss()

def select_action(state, epsilon):
    if random.random() < epsilon:
        return env.action_space.sample()

    with torch.no_grad():
        q_values = policy_net(state.unsqueeze(0))
        return q_values.argmax().item()

def train_step(batch_size, gamma):
    if len(replay_buffer) < batch_size:
        return None

    state, action, reward, state_next, done = replay_buffer.sample(batch_size)

    q_values = policy_net(state)
    q_value = q_values.gather(1, action.unsqueeze(1)).squeeze(1)

    with torch.no_grad():
        next_q = target_net(state_next).max(1)[0]
        target = reward + gamma * next_q * (1 - done)

    loss = loss_fn(q_value, target)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss.item()

epsilon_start = config["epsilon"]["start"]
epsilon_end = config["epsilon"]["end"]
epsilon_decay = config["epsilon"]["decay_steps"]
epsilon = epsilon_start

steps_done = 0

data = []

total_episodes = config["train"]["episodes"]

for episode in range(total_episodes):
    print(f"Episode {episode + 1} is running...")
    state, _ = env.reset(seed=config["env"]["seed"] + episode)
    state = torch.tensor(state, dtype=torch.float32)

    total_reward = 0
    total_steps = 0
    cause_of_termination = "unknown"

    for step in range(config["train"]["max_steps"]):
        epsilon = epsilon_end + (epsilon_start - epsilon_end) * exp(-1. * steps_done / epsilon_decay)
        action = select_action(state, epsilon)

        next_state, reward, terminated, truncated, _ = env.step(action)

        if config["additional_rewards"]["enabled"]:
            reward += config["additional_rewards"]["step"]
            if truncated:
                reward += config["additional_rewards"]["truncation"]

        if config["reward_clipping"]["enabled"]:
            reward_clipped = max(config["reward_clipping"]["min"], min(config["reward_clipping"]["max"], reward))
        else:
            reward_clipped = reward

        done = terminated or truncated

        next_state = torch.tensor(next_state, dtype=torch.float32)

        replay_buffer.push(state, action, reward_clipped, next_state, done)

        loss = train_step(batch_size=config["replay_buffer"]["batch_size"], gamma=config["gamma"])

        state = next_state
        total_reward += reward
        steps_done += 1
        total_steps += 1

        if done:
            if terminated:
                if reward == 100:
                    cause_of_termination = "safe landing"
                elif reward == -100:
                    if state[0] > 1.0:
                        cause_of_termination = "out of viewport"
                    elif state[2] == 0.0 and state[3] == 0.0:
                        cause_of_termination = "sleep"
                    else:
                        cause_of_termination = "crash"
            elif truncated:
                cause_of_termination = "truncation"
            break

    if config["target_update"]["type"] == "hard":
        if episode % config["target_update"]["frequency"] == 0:
            target_net.load_state_dict(policy_net.state_dict())
    elif config["target_update"]["type"] == "soft":
        tau = config["target_update"]["tau"]
        for target_param, param in zip(target_net.parameters(), policy_net.parameters()):
            target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)

    loss_display = loss if loss is not None else 0
    data.append({
        "episode": episode,
        "reward": total_reward,
        "epsilon": epsilon,
        "loss": loss_display,
        "steps": total_steps,
        "termination_cause": cause_of_termination
    })

pd.DataFrame(data).to_csv(config["log_path"], index=False)
torch.save(policy_net.state_dict(), config["save_path"])
