# Modules
import os
from argparse import ArgumentParser

# Utils
from src.utils.get_config import get_config

def get_config_path():
    parser = ArgumentParser(description='Evaluate a trained model on the environment.')
    parser.add_argument('--config', type=str, required=True, help='Path to the evaluation configuration file.')
    args = parser.parse_args()
    return args.config

def eval_model(eval_path, config_name):
    os.makedirs("outputs/logs", exist_ok=True)
    os.system(f"python -m scripts.eval --config {eval_path}")
    os.makedirs("outputs/results", exist_ok=True)
    for seed in range(5):
        log_file = f"outputs/logs/{config_name}_eval_log{seed}.csv"
        if os.path.exists(log_file):
            os.system(f"python -m scripts.analyse --type eval --filename {log_file}")
            os.system("mv " + log_file.replace('.csv', '.png') + " outputs/results/")
        else:
            print(f"Log file {log_file} not found. Skipping analysis for seed {seed}.")


config_path = get_config_path()
config = get_config()

config_name = config["name"]
eval_model(config_path, config_name)
