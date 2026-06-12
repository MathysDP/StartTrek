# heuristic_policy.py

## Purpose

Rule-based policy for a discrete LunarLander action space.

## Inputs

- state layout: [x, y, v_x, v_y, theta, theta_dot, left_leg_contact, right_leg_contact]

## Rule order (first match wins)

1. If both legs are in contact, return 0 (do nothing).
2. If y < 0.7 and v_y < -0.25, return 2 (main engine).
3. If theta_dot < -0.2 and theta < -0.15, return 1 (left engine).
4. If theta_dot > 0.2 and theta > 0.15, return 3 (right engine).
5. If v_y < -0.35, return 2.
6. If theta < -0.25, return 1.
7. If theta > 0.25, return 3.
8. If x < -0.25, return 3.
9. If x > 0.25, return 1.
10. Otherwise, return 0.

## Notes

- The first matching rule is returned; later rules are skipped.
- Assumes actions are in the 0 to 3 range.
- No learning or randomness is used.
