# Modules
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def get_log_path():
    parser = argparse.ArgumentParser(description='Plot training data from a CSV file.')
    parser.add_argument('--type', choices=['train', 'eval'], required=True, help='Type of data to plot (train or eval).')
    parser.add_argument('--filename', type=str, required=True, help='Path to the CSV file containing training data.')
    args = parser.parse_args()
    return args.type, args.filename

def plot_training_data(file_path):
    df = pd.read_csv(file_path)

    plt.style.use('dark_background')

    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    axs[0, 0].plot(df['episode'], df['reward'])
    axs[0, 0].set_title('Reward per Episode')
    axs[0, 0].set_xlabel('Episode')
    axs[0, 0].set_ylabel('Reward')

    axs[0, 1].plot(df['episode'], df['epsilon'])
    axs[0, 1].set_title('Epsilon Decay')
    axs[0, 1].set_xlabel('Episode')
    axs[0, 1].set_ylabel('Epsilon')

    axs[1, 0].plot(df['episode'], df['loss'])
    axs[1, 0].set_title('Loss per Episode')
    axs[1, 0].set_xlabel('Episode')
    axs[1, 0].set_ylabel('Loss')

    axs[1, 1].plot(df['episode'], df['steps'])
    axs[1, 1].set_title('Steps per Episode')
    axs[1, 1].set_xlabel('Episode')
    axs[1, 1].set_ylabel('Steps')

    plt.tight_layout()
    plt.savefig(file_path.replace('.csv', '.png'))

def plot_evaluation_data(file_path):
    df = pd.read_csv(file_path)

    plt.style.use('dark_background')

    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    axs[0, 0].plot(df['episode'], df['rewards'])
    mean_reward = df['rewards'].mean()
    axs[0, 0].axhline(mean_reward, color='#f78152', linestyle='--', label=f'Mean = {mean_reward:.2f}')
    axs[0, 0].set_title('Rewards per Episode')
    axs[0, 0].set_xlabel('Episode')
    axs[0, 0].set_ylabel('Rewards')
    axs[0, 0].legend()

    axs[0, 1].plot(df['episode'], df['steps'])
    axs[0, 1].set_title('Steps per Episode')
    axs[0, 1].set_xlabel('Episode')
    axs[0, 1].set_ylabel('Steps')

    termination_counts = df['termination_cause'].value_counts()

    colors_map = {
        'crash': "#f78152",
        'safe landing': "#30a578",
        'truncation': '#ffd43b',
        'out of viewport': "#861fa3",
    }

    bar_colors = [
        colors_map.get(cause, 'white')
        for cause in termination_counts.index
    ]

    axs[1, 0].bar(termination_counts.index, termination_counts.values, color=bar_colors)
    axs[1, 0].set_title('Termination Causes')
    axs[1, 0].set_xlabel('Cause')
    axs[1, 0].set_ylabel('Count')

    scatter_colors = df['termination_cause'].map(colors_map)

    axs[1, 1].scatter(df['steps'], df['rewards'], c=scatter_colors, alpha=0.7)
    axs[1, 1].set_title('Rewards vs Steps')
    axs[1, 1].set_xlabel('Steps')
    axs[1, 1].set_ylabel('Rewards')

    plt.tight_layout()
    plt.savefig(file_path.replace('.csv', '.png'))

type, file_path = get_log_path()

if type == 'train':
    plot_training_data(file_path)
elif type == 'eval':
    plot_evaluation_data(file_path)