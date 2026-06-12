# DQN_policy.py

## Purpose

Defines a simple MLP Q-network and a policy wrapper that loads weights and returns greedy actions.

## DQN_network

- `__init__`(input_size, output_size, *hidden_sizes)
  - Builds a list of Linear and ReLU layers.
  - If hidden_sizes is empty, defaults to [64].
  - Pattern: Linear -> ReLU for each hidden layer, then a final Linear to output_size.
- forward(x) returns self.model(x).

## DQN_policy

- `__init__`(model_path, input_size, output_size, *hidden_sizes)
  - Creates a DQN_network and loads weights with torch.load(model_path).
  - Sets the network to eval() mode.
- `__call__`(state, env)
  - Converts state to float32 tensor and adds a batch dimension.
  - Uses torch.no_grad() to compute Q-values.
  - Returns the argmax action as an int.

## Inputs and outputs

- Input state shape: 8 values for LunarLander.
- Output action: integer in the 0 to 3 range.

## Usage

from src.policies.DQN_policy import DQN_policy
policy = DQN_policy("outputs/models/baseConfig_model.pth", 8, 4, 128, 256)
action = policy(state, env)

## Notes
- env is unused by the policy but kept for a consistent call signature.
- No explicit device handling; loads on the default torch device.
