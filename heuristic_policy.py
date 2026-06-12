import gymnasium as gym

PREFIX="heuristic_policy"

def policy(obs, env):
    x, y, v_x, v_y, theta, theta_dot, left_leg_contact, right_leg_contact = obs
    if left_leg_contact == 1 and right_leg_contact == 1:
        return 0
    if y < 0.7 and v_y < -0.25:
        return 2
    if theta_dot < -0.2 and theta < -0.15:
        return 1
    if theta_dot > 0.2 and theta > 0.15:
        return 3
    if v_y < -0.35:
        return 2
    if theta < -0.25:
        return 1
    if theta > 0.25:
        return 3
    if x < -0.25:
        return 3
    if x > 0.25:
        return 1
    return 0
