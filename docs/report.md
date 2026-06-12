# Report

This report provides an explanation of our approach to create a **working model for the LunarLander environment**.
A model is considered working if it achieves **an average reward of at least 200 over 100 consecutive episodes**.
It also must be able to be **reproductible**, meaning that over **five different seeds**, the model should achieve the required performance.

## Policy discovery
### [Random policy](random_policy.md)
Firstly, we aimed to understand the environment and its dynamics.
We consequently implemented a random policy to interact with the environment and observe the rewards and state transitions.

![Random evaluation plots 0](../outputs/results/randomConfig_eval_log0.png)

Without surprise, the random policy performed very poorly. It achieved an average reward of around -170.

### [Heuristic policy](heuristic_policy.md)
To improve our understanding of the environment, we implemented a heuristic policy based on the position and velocity of the lander.

![Heuristic evaluation plots 0](../outputs/results/heuristicConfig_eval_log0.png)

The heuristic policy performed better than the random policy, achieving an average reward of around -10. It is still insufficient to consider it a working model.
Contrarily to the random policy, the heuristic policy is able to land successfully the lander in some episodes.

### [DQN policy](DQN_policy.md)
Finally, we implemented a Deep Q-Network (DQN) policy. DQN is a popular reinforcement learning algorithm that uses a neural network to approximate the Q-values of state-action pairs.
The DQN policy is trained using the experience replay technique, which allows the agent to learn from past experiences and improve its performance over time.

## Configuration research
To find a working model, we experimented with different configurations of the DQN policy.

### First configuration
For the [first configuration](../configs/train/initialConfig.yaml), we used common hyperparameters for DQN, such as a learning rate of 0.001, a gamma of 0.99 and a replay buffer size of 50000.

**Training plots**:  
![Initial training plots](../outputs/logs/initialConfig_log.png)

**Manual analysis of the training plots**:
- The rewards per episode increase over time. On the last 100 episodes, the rewards range is around 0 to 300.
- The epsilon value decreases from 1 to around 0.1, in the first 600 episodes, which means that the agent is exploring less and exploiting more as training progresses.
- The loss value fluctuates a little bit, but it generally decreases over time.
- The steps per episode is less than 200, in the first 300 episodes. After that, it increases to 1000 steps per episode, which is the maximum allowed by the environment. This indicates that the agent is struggling to land successfully and is taking longer episodes to learn.

**Evaluation plots**:  
Despite a mid training performance, we evaluate the model to have a reference point for the next configurations. We evaluate the model over 100 episodes on five different seeds.  
![Initial evaluation plots 0](../outputs/results/initialConfig_eval_log0.png)
![Initial evaluation plots 1](../outputs/results/initialConfig_eval_log1.png)
![Initial evaluation plots 2](../outputs/results/initialConfig_eval_log2.png)
![Initial evaluation plots 3](../outputs/results/initialConfig_eval_log3.png)
![Initial evaluation plots 4](../outputs/results/initialConfig_eval_log4.png)

**Conclusion of the first configuration**:  
Just as we expected, the model does not achieve the required performance. The average reward over 100 episodes is around 130, which is below the threshold of 200.
We can notice that around 60% of the episodes end with a safe landing, that is a good point, but the remaining 1/3 of the episodes end with a crash or a truncation, which significantly reduces the average reward.
The performance is also not consistent across the different seeds, which indicates that the model is not robust.

## Second configuration
For the [second configuration](../configs/train/secondConfig.yaml), we made some adjustments to the hyperparameters based on the insights from the first configuration.
In order to reach the moment where the model stops to make long episodes, that conduct to a truncation, we increased the number of episodes to 2000.

**Training plots**:  
![Second training plots](../outputs/logs/secondConfig_log.png)

**Manual analysis of the training plots**:
- As expected, the results are similar to the first configuration in the first 1500 episodes. After that, we can see that the model seems to learn better because the steps per episode decreases.
- The decrease of steps per episode just begins at the end of the training, it has certainly not enough experience at the moment.

**Evaluation plots**:  
To support our analysis, we evaluate again the model over 100 episodes on five different seeds.  
![Second evaluation plots 0](../outputs/results/secondConfig_eval_log0.png)
![Second evaluation plots 1](../outputs/results/secondConfig_eval_log1.png)
![Second evaluation plots 2](../outputs/results/secondConfig_eval_log2.png)
![Second evaluation plots 3](../outputs/results/secondConfig_eval_log3.png)
![Second evaluation plots 4](../outputs/results/secondConfig_eval_log4.png)

**Conclusion of the second configuration**:  
The increase in the number of episodes allowed the model to learn better. It reaches an average reward of around 210, that makes it a working model for the LunarLander environment.
However, the performance is too close to the threshold and varies over the different seeds. We will try to fix it in the next configuration.
We also notice that crashes are strictly more frequent in the second configuration than in the first one, but the truncations are still present.

## Third configuration
For the [third configuration](../configs/train/thirdConfig.yaml), we made further adjustments to the hyperparameters based on the insights from the second configuration.
In order to reduce the number of truncations, we add a penalty of **-200** for each truncation and **-0.2** for each step taken.

We have tested several penalties for truncation and steps.
When we put larger penalties, the model focuses too much on avoiding truncations and conversely, when we put smaller penalties, the model continues to make long episodes and does not learn to land successfully.
We found that the chosen penalties are a **good balance** between these two extremes, as they encourage the model to avoid truncations while still allowing it to explore and learn from its mistakes.

**Training plots**:  
![Third training plots](../outputs/logs/thirdConfig_log.png)

**Manual analysis of the training plots**:
- All the plots have changed significantly compared to the previous configurations.
- The rewards per episode range seems to be more concentrated at the end of the training.
- The number of steps per episode decreases early in the training, which indicates that the penalty for truncation is effective in reducing the number of long episodes.

**Evaluation plots**:  
To support our analysis, we evaluate again the model over 100 episodes on five different seeds.  
![Third evaluation plots 0](../outputs/results/thirdConfig_eval_log0.png)
![Third evaluation plots 1](../outputs/results/thirdConfig_eval_log1.png)
![Third evaluation plots 2](../outputs/results/thirdConfig_eval_log2.png)
![Third evaluation plots 3](../outputs/results/thirdConfig_eval_log3.png)
![Third evaluation plots 4](../outputs/results/thirdConfig_eval_log4.png)

**Conclusion of the third configuration**:  
The model achieves an average reward of around 245, which is above the threshold of 200.
The performance is more consistent across the different seeds, which indicates that the model is more robust.
The number of truncations is significantly reduced, which confirms the effectiveness of the penalty for truncation.
Overall, the third configuration is considered a working model for the LunarLander environment, as it achieves the required performance and is reproducible across different seeds.

### Final configuration
Even if we have a working model, we try to have a better one by modifying more complex hyperparameters.
We make several adjustments to the hyperparameters based on the insights from the third configuration and we obtain a [final configuration](../configs/train/finalConfig.yaml) that achieves an average reward of around 255, which is significantly above the threshold of 200.

**Training plots**:  
![Final training plots](../outputs/logs/finalConfig_log.png)

**Evaluation results**:  
![Final evaluation plots 0](../outputs/results/finalConfig_eval_log0.png)
![Final evaluation plots 1](../outputs/results/finalConfig_eval_log1.png)
![Final evaluation plots 2](../outputs/results/finalConfig_eval_log2.png)
![Final evaluation plots 3](../outputs/results/finalConfig_eval_log3.png)
![Final evaluation plots 4](../outputs/results/finalConfig_eval_log4.png)

**Conclusion of the final configuration**:  
As the third model, the final configuration creates a working model for the LunarLander environment, as it achieves the required performance and is reproducible across different seeds.
The performance is even better than the third configuration, as it achieves an average reward of around 255, which is significantly above the threshold of 200.

### Fourth configuration
As said before, between the third and the final configuration, we made several adjustments to the hyperparameters based on the insights from the third configuration.
We notably trained the model with the fourth configuration, where we increased the number of episodes and the decay of epsilon, in order to give more time to the model to learn and to explore the environment.

**Training plots**:  
![Fourth training plots](../outputs/logs/fourthConfig_log.png)

**Evaluation results**:  
![Fourth evaluation plots 0](../outputs/results/fourthConfig_eval_log0.png)
![Fourth evaluation plots 1](../outputs/results/fourthConfig_eval_log1.png)
![Fourth evaluation plots 2](../outputs/results/fourthConfig_eval_log2.png)
![Fourth evaluation plots 3](../outputs/results/fourthConfig_eval_log3.png)
![Fourth evaluation plots 4](../outputs/results/fourthConfig_eval_log4.png)

**Conclusion of the fourth configuration**:  
We can see that this model is worse than the one with the third configuration. Nevertheless, when we modified others hyperparameters, we can obtain the final configuration that is better than the third one.
This shows that the hyperparameters are interdependent and that it is important to find the right balance between them to achieve the best performance.

## Others hyperparameters
In addition to the below configurations, we also experimented to modify some hyperparameters, but we did not find any significant improvement in the performance of the model, on the contrary, some modifications led to a decrease in performance.

### Epsilon
We have experimented with different values of epsilon decay, but we always trained the model with an initial epsilon of **1** and a final epsilon of **0.05**.
We found that the start must always be 1 because at the beginning of the training, the model has no experience and needs to explore the environment to learn.
We also found that the end defined at 0.05 is a good choice, as it allows the model to continue to explore the environment in 5% of the time.

### Replay buffer batch size
The increase of the replay buffer batch size is a common technique to improve the performance of DQN models, as it allows the model to learn from a larger number of experiences at each training step.
However, in our case, it did not lead to a significant improvement in the performance of the model. In fact, it even led to a decrease in performance, as the model was not able to learn effectively from the larger batches of experiences.

### Target network update
There are two common techniques to update the target network in DQN: the **hard update** and the **soft update**.
The hard update consists in copying the weights of the main network to the target network every fixed number. The soft update consists in updating the weights of the target network as a weighted average of the weights of the main network and the target network.
We experimented with both techniques, but we did find any working configuration with the soft update.

### Gamma (discount factor)
The gamma parameter controls the importance of future rewards. We experimented with different values of gamma, but we found that a value of 0.99 is a good choice, as it allows the model to consider the long-term consequences of its actions.
Moreover, we add penalty for truncation and steps, we consequently need to have a high gamma to allow the model to learn from these penalties and adjust its behavior accordingly.

### Reward clipping
Reward clipping consists in clipping the rewards to a certain range, such as [-1, 1]. This technique is often used to stabilize the training of DQN models, as it prevents the model from receiving very large rewards that can lead to unstable learning.
However, in our case, we found that reward clipping did not lead to an increase in performance. The model was able to make the difference between an important positive reward as a safe landing and a common positive reward as a leg in contact with the ground, which is crucial for learning to land successfully.

## Limits
Despite the success of our final configuration, there are still some limits to our approach:
- The model is still not able to achieve a perfect score of 100 safely landing the lander in all episodes. There are still some crashes and truncations, even if they are significantly reduced.
- The model must be trained for a long time (2200 episodes) to achieve the required performance, which can be computationally expensive.

## Future work
If we had more time, we would like to:
- Explore other algorithms, sush as PPO.
- Train the model with a more complex environment. We could add winds of different intensities, a different gravity...
- Optimize our model in order to have a stable performance with a lower training time.

## Notes
- The training is different from one computer to another, even with the same configuration. This is due to the fact that the training process is not deterministic and can be affected by various factors such as the hardware, the software and the random number generator.
- The evaluation is not different from one computer to another, as long as the same seeds are used. This is because the evaluation process is deterministic and only depends on the model and the environment.
