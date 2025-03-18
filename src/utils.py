"""
utils.py

Utility functions for parsing data, computing pulse intervals, and plotting results.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_pulses(csv_path: str) -> pd.DataFrame:
    """
    Loads pulse data from a CSV file.

    Args:
        csv_path (str): Path to the CSV file (e.g. data/sample_signals.csv).

    Returns:
        pandas.DataFrame: DataFrame containing at least 'time' and 'amplitude' columns.
    """
    df = pd.read_csv(csv_path)
    # Ensure DataFrame has required columns. Throw an error if missing.
    required_cols = ["time", "amplitude"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    # Sort by time if not already
    df = df.sort_values(by="time").reset_index(drop=True)
    return df

def plot_pulses(df: pd.DataFrame, title: str = "Pulse Train"):
    """
    Plots the pulse amplitude over time.

    Args:
        df (pandas.DataFrame): DataFrame with 'time' and 'amplitude' columns.
        title (str): Plot title.
    """
    plt.figure(figsize=(8, 4))
    plt.scatter(df["time"], df["amplitude"], marker='x', color='blue', label='Pulses')
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_deinterleaved_tracks(track_assignments, times, amps):
    """
    Plots separated pulse tracks with different colors.

    Args:
        track_assignments (list[int]): List of track indices for each pulse.
        times (np.array): Array of time values.
        amps (np.array): Array of amplitude values.
    """
    unique_tracks = np.unique(track_assignments)
    plt.figure(figsize=(8, 4))
    for track_id in unique_tracks:
        idx = np.where(track_assignments == track_id)
        plt.scatter(times[idx], amps[idx], label=f"Track {track_id}")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title("Deinterleaved Pulse Trains")
    plt.grid(True)
    plt.legend()
    plt.show()
