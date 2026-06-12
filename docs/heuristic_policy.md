# heuristic_policy.py

## Purpose
Rule-based policy for a discrete LunarLander action space.

## Usage
```python
from src.policies.heuristic_policy import heuristic_policy

# create an instance of the heuristic policy
policy = heuristic_policy()

# get an action by calling the policy with the current state and environment
action = policy(state, env)
```

## Description
The **heuristic_policy** function returns a policy function that takes the current state and environment as input and returns an action based on a set of predefined rules.
The policy uses the state information (such as position, velocity, angle and leg contact) to determine which action to take in order to land the lunar module safely.
The rules are evaluated in a specific order, and the first matching rule determines the action returned by the policy.
This policy does not learn from the environment and does not use any randomness; it is purely deterministic based on the defined rules. It serves as a simple heuristic approach to the LunarLander problem, which can be used for comparison with learning-based policies.
No initialization is needed for this policy, as it does not maintain any internal state or parameters.

## Inputs and state layout
The policy takes the current state and environment as input. The state is expected to be a vector with the following layout:
- **x**: horizontal position
- **y**: vertical position
- **v_x**: horizontal velocity
- **v_y**: vertical velocity
- **theta**: angle
- **theta_dot**: angular velocity
- **left_leg_contact**: whether the left leg is in contact with the ground (0 or 1)
- **right_leg_contact**: whether the right leg is in contact with the ground (0 or 1)

## Output and action space
The policy returns an action based on the following discrete action space:
- **0**: do nothing
- 1: fire left engine
- 2: fire main engine
- 3: fire right engine

## Rule order (first match wins)
1. If both legs are in contact, return 0 (do nothing).
2. If y < 0.7 and v_y < -0.25, return 2 (main engine).
3. If theta_dot < -0.2 and theta < -0.15, return 1 (left engine).
4. If theta_dot > 0.2 and theta > 0.15, return 3 (right engine).
5. If v_y < -0.35, return 2 (main engine).
6. If theta < -0.25, return 1 (left engine).
7. If theta > 0.25, return 3 (right engine).
8. If x < -0.25, return 3 (right engine).
9. If x > 0.25, return 1 (left engine).
10. Otherwise, return 0 (do nothing).

## Objective
This policy is supposed to be done after the random policy and before the DQN policy. It has for objective to discover us the state layout and the action space and to give us a simple baseline to compare with the DQN policy.
