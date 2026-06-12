# START TREK PROJECT

## Project goal

The Star Trek project aim is to design and train a **Reinforcement Learning** agent to land a lunar module in a 2D simulation. To accomplish this task we choose to make a deep Q-network (DQN) algorithm.

## How to setup the project

### Prerequisites

- Python v3+

### Python Dependencies

To install all the python dependencies, we recommend you to :

- create a virtual environnement :
```bash
    $> python3 -m venv .venv && source .venv/bin/activate
```

- and use the requirements.txt file:
```bash
    (.venv) $> pip install -r requirements.txt
```

## How to use the project

- For training :
```bash
    $> python -m scripts.train --config configs/train/baseConfig.yaml
```

- For evaluation :
```bash
    $> python -m scripts.eval --config configs/simpleEval.yaml
```
- For graphics analytics :
```bash
    $> python3 scripts/analyse_policy.py --type train --filename outputs/logs/baseConfig_log.csv
```
or
```bash
    $> python3 scripts/analyse_policy.py --type eval --filename outputs/logs/baseConfig_eval_log.csv
```

All theses commands will generate outputs in the outputs/logs directory.
See more details on the docs directory.

## Contributors

Naëlle Guerin, Mato Urbanac and Mathys Dupont.
