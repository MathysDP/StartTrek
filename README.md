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
    $> python -m scripts.eval --config configs/eval/simpleEval.yaml
```
- For graphics analytics :
```bash
    $> python -m scripts.analyse --type train --filename outputs/logs/baseConfig_log.csv
```
or
```bash
    $> python -m scripts.analyse --type eval --filename outputs/logs/baseConfig_eval_log0.csv
```

Outputs are written to outputs/logs and outputs/videos. Analysis PNGs are saved next to the CSV logs.
See more details on the docs directory.

## Contributors

Naëlle Guerin, Mato Urbanac and Mathys Dupont.
