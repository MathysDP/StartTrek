# get_config.py

## Purpose

Parses a required --config argument and loads a YAML config file.

## Function

- get_config() -> dict

## How it works

1. Build an argparse.ArgumentParser().
2. Add --config as a required string argument.
3. parser.parse_args() validates the CLI and produces args.config.
4. Open the file path and call yaml.safe_load().
5. Return the resulting dict.

## Usage

```python
from src.utils.get_config import get_config

config = get_config()
```

## Inputs

- --config: path to YAML config file (required)

## Outputs

- Returns a Python dict from yaml.safe_load().

## Notes

- Missing --config triggers an argparse error and exits.
- Invalid paths or invalid YAML will raise an exception at load time.
