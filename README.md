# START TREK PROJECT

## Project goal
The Star Trek project aim is to design and train a **Reinforcement Learning** agent to land a lunar module in a 2D simulation. To accomplish this task we choose to make a deep Q-network (DQN) algorithm.

## How to setup the project
### Prerequisites
- Python v3+

### Python Dependencies
To install all the python dependencies, we recommend you to:
- Create a virtual environnement:
```bash
$> python3 -m venv .venv && source .venv/bin/activate
```
- Then, install the requirements thanks to requirements.txt:
```bash
(.venv) $> pip install -r requirements.txt
```

## How to use the project
### Training
A agent can be trained with the following command:
```bash
(.venv) $> python -m scripts.train --config configs/train/<config_name>.yaml
```
By convention, the training config file should be in the **configs/train** directory and should have a name that describes the training configuration.

### Evaluation
A agent can be evaluated with the following command:
```bash
(.venv) $> python -m scripts.eval --config configs/eval/<config_name>.yaml
```
By convention, the evaluation config file should be in the **configs/eval** directory and should have a name that describes the evaluation configuration.

### Analysis
Training and evaluation scripts create CSV logs in the **outputs/logs** directory. These logs can be analysed with the first command for training logs and the second one for evaluation logs:
```bash
(.venv) $> python -m scripts.analyse --type train --filename outputs/logs/<config_name>_log.csv
```
```bash
(.venv) $> python -m scripts.analyse --type eval --filename outputs/logs/<config_name>_eval_log<seed>.csv
```
To know that the training and evaluation logs don't contain the same information, that why we need to specify the type of log we want to analyse. The analysis script will create PNG files with different plots to help you understand the training and evaluation process.
A training generate one log file with the suffix **_log.csv** and an evaluation generate five log files with the suffix **_eval_logX.csv** where X is the seed that was used for the evaluation.

### One shot evaluation
A agent can be evaluated in one shot with the following command:
```bash
(.venv) $> python -m scripts.eval_and_analyse --config configs/eval/<config_name>.yaml
```
Concretly, this command will run the evaluation of the agent and make the analysis for its five seeds.

## More information
You can consult detailed explanations about our implementation in the **docs** directory.
You can also find the different configurations we used for training and evaluation in the **configs** directory and their results in the **outputs** directory.

## Contributors
Naëlle Guerin, Mato Urbanac and Mathys Dupont.
