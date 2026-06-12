# random_policy.py

## Purpose
Baseline policy that samples random actions from the environment, ignoring the state.

## Usage
```python
from src.policies.random_policy import random_policy

# create an instance of the random policy
policy = random_policy()

# get an action by calling the policy with the current state and environment
action = policy(state, env)
```

## Description
The **random_policy** function returns a policy function that takes the current state and environment as input and returns a random action sampled from the environment's action space.
This policy does not use the state information at all and simply samples actions uniformly at random.
It serves as a simple baseline for comparison with more sophisticated policies that learn from the environment.
The **env** parameter is included in the policy function signature to maintain a consistent interface with other policies that may require access to the environment for action selection, even though it is not used in this random policy.
No initialization is needed for this policy, as it does not maintain any internal state or parameters.

## Objective
This policy is supposed to be done first, before the heuristic policy and the DQN policy. It has for objective to discover us the environment, without having to understand the state layout or the action space.