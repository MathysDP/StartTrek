import torch
import torch.nn as nn

PREFIX="DQN_policy"

class DQN(nn.Module):
    def __init__(self):

        super(DQN, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(8, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 4)
        )

    def forward(self, x):
        return self.model(x)
    
def policy(obs, env):
    obs = torch.tensor(obs, dtype=torch.float32)
    with torch.no_grad():
        action = DQN().forward(obs).argmax().item()
    return action
