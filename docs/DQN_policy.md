# DQN_policy.py

## Purpose
Defines a simple MLP Q-network and a policy wrapper that loads weights and returns greedy actions.

## Usage
```python
from src.policies.DQN_policy import DQN_policy

# create an instance of the DQN policy with the path to the saved model and network architecture parameters
policy = DQN_policy("outputs/models/<config_name>_model.pth", 8, 4, 128, 256)

# get an action by calling the policy with the current state and environment
action = policy(state, env)
```

## DQN_network
### Initialization
The DQN_network class is a **PyTorch nn.Module** that defines a multi-layer perceptron (MLP) for approximating Q-values.
The initialization method takes the **input size**, **output size** and an optional list of **hidden layer sizes**. If no hidden sizes are provided, it defaults to a single hidden layer of size 64.
The network is built as a sequence of Linear and ReLU layers for each hidden layer.

For example, if the input size is 8, output size is 4, and hidden sizes are [128, 256], the architecture will be:  
**Linear(8, 128) -> ReLU -> Linear(128, 256) -> ReLU -> Linear(256, 4)**

### Forward method
The forward method takes an input tensor and passes it through the defined model, returning the output tensor of Q-values for each action.

## DQN_policy
### Initialization
The DQN_policy class is a wrapper around the DQN_network that loads pre-trained weights from a specified model path.
The initialization method creates an instance of DQN_network with the given input size, output size and hidden sizes, then loads the weights using **torch.load()** and sets the network to evaluation mode with **eval()**.

### Call method
The call method takes the current state and environment as input, converts the state to a float32 tensor and adds a batch dimension.
It then computes the Q-values using the network in a no-gradient context (with **torch.no_grad()**) and returns the action with the highest Q-value as an integer.

State and environment are expected to be compatible with the LunarLander environment, where the state is an 8-dimensional vector and the action space consists of 4 discrete actions.
You can understand more about the state layout and action space in the [heuristic policy guide](heuristic_policy.md).

## Objective
This policy is supposed to be done after the random policy and the heuristic policy. It is the final policy that we want to evaluate and compare with the baselines.
It has for objective to show us how well a DQN agent can perform on the LunarLander environment after being trained with the settings defined in the configuration file used for training.

## Notes
- No explicit device handling; loads on the default torch device.
