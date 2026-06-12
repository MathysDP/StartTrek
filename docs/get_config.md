# get_config.py

## Purpose
Parses a required --config argument and loads a YAML config file.

## Usage
```python
from src.utils.get_config import get_config

config = get_config()
```

## Description
This function uses **ArgumentParser()** from the **argparse** library to parse a required **--config** argument, which should be a path to a YAML file.
If the **--config** argument is missing, **argparse** will automatically print an error message and exit the program.
If the argument is provided, it opens the specified file path and loads the YAML content using **safe_load()** from the **yaml** library.
Finally, it returns the resulting dictionary containing the configuration parameters.

This function checks so that the user provides a config file and that the file is a valid YAML file. If any of these conditions are not met, it will raise an error.

## Used in
- scripts/train.py
- scripts/eval.py
- scripts/eval_and_analyse.py
