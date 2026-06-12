# Train explaination

### Import
- gynasium: for the environment
- argparse: for parsing command line arguments
- yaml: for loading the configuration file
- random: for random number generation
- collections.deque: for the replay buffer
- torch: for building and training the neural network
- torch.nn: for defining the neural network architecture
- torch.optim: for optimization algorithms

### Get configuration
1. parse arguments -> get config file path which is after --config
-> create a helper when bad argument is given
2. open and transform the yaml file into a dictionary

### environment
- create the environment using gym.make()
all the parameters are in the config file

### replay buffer
it is the memory of the agent
we store `state, action, reward, next_state, done` in a deque with a maximum capacity (given in the config file)
utility of deque: when the buffer is full, the oldest transition is removed
the capacity must be large enough to store a good amount of experience, but not too large to consume too much memory

constructor: create a deque with the given capacity

push method: add a transition to the buffer

sample method: randomly sample a batch of transitions from the buffer
the batch size is given in the config file
why: random sampling breaks the correlation between consecutive transitions, which helps to stabilize training

example: we have exp 1, exp 2, exp 3, exp 4, exp 5 in the buffer
if we sample a batch of size 2, we might get exp 1 and exp 4,
which are not consecutive, thus breaking the correlation

state, action, reward, next_state, done = zip(*batch) : unzip the batch into separate lists for states, actions, rewards, next_states, and done flags
example: if batch = [(s1, a1, r1, s1', d1), (s2, a2, r2, s2', d2)]
then state = (s1, s2), action = (a1, a2), reward = (r1, r2), next_state = (s1', s2'), done = (d1, d2)

state = torch.stack([torch.tensor(x, dtype=torch.float32) for x in state]):
convert the list of states into a tensor
pythor can't work with lists, it needs tensors, it's why we convert the list of states into a tensor
the same is done for next_state, action, reward, and done

remember that state (and next_state) is a vector of 8 values, action is an integer, reward is a float, and done is a boolean
it's why we torch.stack after converting each element into a tensor of the appropriate type

__len__ method: return the current size of the buffer

### Neural Network
creation of the "brain" of agent

nn.Module is the base class for all neural networks in PyTorch
init of the base class with super().__init__()
benefit:
- train() and eval() methods for switching between training and evaluation modes
- state_dict() method for saving and loading model parameters

- constructor:
shift from vector of 8 values to a vector of 128 values
then shift from vector of 128 values to a vector of 256 values
then shift from vector of 256 values to a vector of 4 values
last 4 values represent the Q-values for each action (0, 1, 2, 3)
the highest value among the 4 ones is the action to take

reLu: it's activation function
-> without it, the model is linear and consequently not able to learn complex patterns

- forward method:
q_values = model(state)   ==   q_values = model.forward(state)
it's necessary to define the forward method because
it specifies how the input data travels through the network and produces the output

policy_net: the network that we train // the main network
we update it after each action
mode train() allows severial things but i think we didn't activate any of them, so it doesn't change anything

target_net: the 2nd network
we update it less frequently than the policy_net

at initialization, we copy the parameters of policy_net to target_net
then we update target_net with policy_net parameters every config["train"]["target_update"] episodes (cf training loop)

target_net is in eval() mode because we don't want to update its parameters
during training, we only want to use it to compute the target Q-values

in eval mode: no update
in train mode: update

opmizer: we use Adam optimizer, which is an adaptive learning rate optimization algorithm
it computes individual learning rates for each parameter, which can lead to faster convergence compared to standard stochastic

1st parameter: the parameters of the policy_net that we want to optimize
2nd parameter: the learning rate given in the config file config["train"]["learning_rate"]
when a learning rate is too high, the model may diverge and fail to learn = a bad learning
when a learning rate is too low, the model may take a long time to converge = a long time to learn
the learning rate is beetween 0 and 1
often set to 0.001 or 0.0001

loss_fn = nn.MSELoss() : mean squared error loss function

???

### selection of action
we make a random number between 0 and 1
if the number is less than epsilon, we take a random action -> exploration
else we take the action with the highest Q-value -> exploitation

torch.no_grad() is used to disable gradient calculation during action selection
-> reduces memory consumption and speeds up computations
we don't need gradients when we select an action
we only need them during the training step when we update the policy_net parameters

state.unsqueeze(0) convert the state from a 1D tensor of shape (8,) to a 2D tensor of shape (1, 8)
our network can predict Q-values only with a 2D tensor as input

### training step
in select_action(), the agent doesn't learn
this function is consequently a sort of update of network parameters

if len(replay_buffer) < config["train"]["batch_size"],
we don't have enough experience to sample a batch, so we skip the training step

we get a batch of transitions from the replay buffer

we compute the current Q-values for the actions taken in the batch using the policy_net
so we have config["train"]["batch_size"] Q-values

this enables us to get the Q value of the action taken in the batch
-> in the batch, we have the action taken but we don't have the value of the Q

mode torch.no_grad() because we just want to compute the target Q-values, we don't want to update the target_net parameters
we get the maximum Q-value for the next states using the target_net
we build the target `target = reward + gamma * next_q * (1 - done)`
reward is the immediate reward received after taking the action
next_q is the maximum Q-value for the next state
done is a boolean that indicates if the episode has ended
if done is True, it means the episode has ended, so we don't want to add the future reward,
thus we multiply next_q by (1 - done) which will be 0 if done is True and 1 if done is False

gamma is the discount factor, it determines how much the agent values future rewards compared to immediate rewards
a gamma close to 0 makes the agent focus on immediate rewards,
while a gamma close to 1 makes the agent consider future rewards more strongly

loss = loss_fn(current_q, target): calculate of difference between current Q-values and target Q-values
example: if current_q = [1.0, 5.0, 6.0] and target = [3.0, 2.5, 3.5]
then loss = ((1.0 - 3.0)^2 + (5.0 - 2.5)^2 + (6.0 - 3.5)^2) / 3 = 5.5

we want to have the lower loss possible

zero_grad() is used to reset the gradients of the model parameters before backpropagation

loss.backward() ajust the model parameters based in order to minimize the loss
-> we have now new gradients for each parameter of the policy_net

optimizer.step() performs a single optimization step (parameter update) based on the current gradients

loss.item() gives the scalar value of the loss
can be useful for logging

definition gradient: it's the direction and rate of change for reducing the loss
example:
objectif: w = 5 & loss = 0
if w = 2, loss = (w - 5)^2 = 9
gradient = loss derivative = 2 * (w - 5) = -6
interpretation: gradient is negative, so we need to increase w to reduce the loss
||gradient|| = 6: it's large so we can make a big step to update w
learning rate = 0.1
update of w: w = w - learning_rate * gradient = 2 - 0.1 * (-6) = 2 + 0.6 = 2.6
after the update, w is closer to 5 and the loss is reduced to (2.6 - 5)^2 = 5.76
...

### epsilon
this number represents the exploration rate
it starts at config["epsilon"]["start"] so the agent took random actions at the beginning of training
then it decreases over time until it reaches a minimum value (given in the config file)
when epsilon is 0.5, a random action is taken 50% of time randomly and
50% of time the action with the highest Q-value is taken, with the memory and what the agent has learned before

### training loop
we repeat config["train"]["episodes"] times:
for each episode:
1. reset the environment and get the initial state

all states are converted to tensors of type float32 because our network can only work with tensors
reward, action, done are also converted to tensors but in the sample method of the replay buffer
not here, because it's not necessary

we don't care about the info in training, we put _ to ignore it
we will use it in eval

step loop
a max number of steps is given in the config file config["train"]["max_steps"], in order to avoid infinite loops
for each step:
1. select an action according to current state and epsilon

2. execute the action in the env, we receive the next_state, reward, terminated, truncated, info
again we ignore info for training

3. store state, action, reward, next_state, done in the replay buffer
it's called a transition
done is a bool that indicated if the episode is finished
an episode is finished when terminated or truncated is true

4. train the model (cf. training step)



end of episode:
- update of epsilon
we decrease epsilon /!\ to fix because i think we must decrease epsilon with the samely way
if episode < 100 -> ...
elif epsisode < 300 -> ...
else -> ...

/!\ A REFAIRE

every config["train"]["target_update"] episodes, we update the target_net with the policy_net parameters
objecive: stabilize training by keeping a fixed target for a while

we print the episode stats


### docs:
https://docs.pytorch.org/tutorials/intermediate/reinforcement_q_learning.html