# random_policy.py

## Purpose

Baseline policy that samples random actions from the environment, ignoring the state.

## Behavior

- `__call__`(state, env) returns env.action_space.sample().
- No internal state, no training, no configuration.

## Usage

from src.policies.random_policy import random_policy
policy = random_policy()
action = policy(state, env)

## Notes

- Useful for sanity checks or as a simple baseline.
- The env parameter is required because policies share the same call signature.
