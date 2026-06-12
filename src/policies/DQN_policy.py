# Modules
import torch
import torch.nn as nn

class DQN_network(nn.Module):
    def __init__(self, input_size, output_size, *hidden_sizes):
        super().__init__()

        layers = []

        if not hidden_sizes:
            hidden_sizes = [64]

        layers.append(nn.Linear(input_size, hidden_sizes[0]))
        layers.append(nn.ReLU())

        for i in range(len(hidden_sizes) - 1):
            layers.append(nn.Linear(hidden_sizes[i], hidden_sizes[i + 1]))
            layers.append(nn.ReLU())

        layers.append(nn.Linear(hidden_sizes[-1], output_size))

        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)

class DQN_policy:
    def __init__(self, model_path, input_size, output_size, *hidden_sizes):
        self.network = DQN_network(input_size, output_size, *hidden_sizes)
        self.network.load_state_dict(torch.load(model_path))
        self.network.eval()

    def __call__(self, state, env):
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            q_values = self.network(state_tensor)
            return q_values.argmax().item()
