# eval_and_analyse.py

## Purpose
Runs evaluation and generates plots for the five evaluation logs.

## Usage
```bash
python -m scripts.eval_and_analyse --config configs/eval/<config_name>.yaml
```

## Command-line arguments
As above, the script takes one required argument:
- **--config**: required, path to the evaluation YAML config file.

## Description
This script combines evaluation and analysis steps.
It first runs the evaluation using the specified config, which generates five CSV logs in **outputs/logs** with the naming pattern **<config_name>_eval_log<seed>.csv**.
Then, it looks for these log files and generates PNG plots for each one using the **analyse.py** script.
The generated PNG files are saved in **outputs/results** with the same base name as the CSV logs.
For example, if the evaluation with the seed 0 generates five CSV logs in **outputs/logs/** named **<config_name>_eval_log<seed>.csv**, where seed takes the values 0 to 4, the script will generate five corresponding PNG files in **outputs/results/** named **<config_name>_eval_log<seed>.png**.

## Notes
- More precised description of the evaluation and analysis process can be found in the [evaluation guide](eval.md) and the [analysis guide](analyse_policy.md), respectively.
