# eval_and_analyse.py

## Purpose

Runs evaluation and generates plots for each eval log, then collects PNGs in outputs/results.

## Usage

```bash
python -m scripts.eval_and_analyse --config configs/eval/simpleEval.yaml
```

## CLI parsing

- get_args() parses a required --config argument (path to the eval YAML).
- get_config() loads the same YAML so the script can read config["name"].

## Flow

1. Create outputs/logs if missing.
2. Run evaluation with:
   - python -m scripts.eval --config <eval_path>
3. Create outputs/results if missing.
4. For seed in range(5):
   - Look for outputs/logs/<name>_eval_log<seed>.csv
   - If found, run:
     - python -m scripts.analyse --type eval --filename <log_file>
   - Move the PNG to outputs/results
   - If missing, print a skip message

## Outputs

- CSV logs: outputs/logs/<name>_eval_log<seed>.csv
- Analysis PNGs: outputs/results/<name>_eval_log<seed>.png
- Videos (from eval): outputs/videos

## Notes

- The log suffix is 0..4 because the script loops range(5).
- Evaluation and analysis are executed via os.system, so the active Python environment is used.
