# Modules
import gymnasium as gym
import torch
import torch.nn as nn
import torch.optim as optim

# Utils
import random
from collections import deque
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

random.seed(config["env"]["seed"])

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

epsilon = config["epsilon"]["start"]
epsilon_min = config["epsilon"]["end"]

for episode in range(config["train"]["episodes"]):
    state, _ = env.reset(seed=config["env"]["seed"] + episode)
    state = torch.tensor(state, dtype=torch.float32)

    total_reward = 0

    for t in range(config["train"]["max_steps"]):
        action = select_action(state, epsilon)

        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        next_state = torch.tensor(next_state, dtype=torch.float32)

        replay_buffer.push(state, action, reward, next_state, done)

        loss = train_step(batch_size=config["replay_buffer"]["batch_size"], gamma=config["gamma"])

        state = next_state
        total_reward += reward

        if done:
            break

    if episode < 100:
        epsilon = epsilon
    elif episode < 300:
        epsilon = max(epsilon_min, epsilon * 0.998)
    else:
        epsilon = max(epsilon_min, epsilon * 0.995)

    if episode % config["target_update"]["frequency"] == 0:
        target_net.load_state_dict(policy_net.state_dict())

    print(f"Episode {episode} | Reward: {total_reward:.2f} | Epsilon: {epsilon:.3f}")

torch.save(policy_net.state_dict(), config["save_path"])
