# analyse.py

## Purpose

Generates diagnostic plots from training or evaluation CSV logs and saves PNG files.

## Usage

```bash
	python -m scripts.analyse --type train --filename outputs/logs/baseConfig_log.csv
	python -m scripts.analyse --type eval --filename outputs/logs/baseConfig_eval_log0.csv
```

## CLI parsing

- get_log_path() uses argparse with two required flags:
	- --type: "train" or "eval"
	- --filename: path to the CSV log file
- Returns (type, filename) and drives which plotting function is called.

## Train plots (plot_training_data)

- Loads the CSV into a pandas DataFrame.
- Creates a 2x2 grid:
	- Reward per episode
	- Epsilon decay
	- Loss per episode
	- Steps per episode
- Saves PNG as file_path with .csv replaced by .png.

## Eval plots (plot_evaluation_data)

- Loads the CSV into a pandas DataFrame.
- Creates a 2x2 grid:
	- Rewards per episode + mean reward line
	- Steps per episode
	- Termination cause counts (bar chart)
	- Rewards vs steps (scatter colored by cause)
- Uses a color map:
	<span style="padding:px;background-color:#f78152"> - crash</span>
	<span style="padding:px;background-color:#30a578"> - safe landing</span>
	<span style="padding:px;background-color:#ffd43b"> - truncation</span>
	<span style="padding:px;background-color:#861fa3"> - out of viewport</span>
  - Any other cause (for example "sleep") is colored white.

## Outputs

- PNG saved next to the CSV (same base name).

## Expected columns

- Train: episode, reward, epsilon, loss, steps (extra columns are ignored)
- Eval: episode, rewards, steps, termination_cause

## Notes

- Uses matplotlib dark_background style.
- Does not display figures; it only saves them.
