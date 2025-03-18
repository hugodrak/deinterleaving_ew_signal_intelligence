"""
deinterleave.py

Command-line script for deinterleaving pulses from multiple emitters.
A very basic algorithm is demonstrated: time-based grouping using
pulse repetition interval (PRI) analysis or a threshold-based approach.
"""

import argparse
import numpy as np
import pandas as pd
from utils import load_pulses, plot_deinterleaved_tracks

def simple_time_based_deinterleave(times: np.ndarray, threshold: float = 0.02) -> np.ndarray:
    """
    A naive approach that groups pulses into different tracks if the gap between
    consecutive pulses is larger than some threshold (simulating a possible PRI).
    This is just a demonstration; real deinterleaving can be much more complex.

    Args:
        times (np.array): Sorted array of pulse times.
        threshold (float): Time gap threshold used for grouping.
    
    Returns:
        track_assignments (np.array): An array of track indices for each pulse.
    """
    track_assignments = np.zeros_like(times, dtype=int)
    current_track = 0
    track_assignments[0] = current_track

    for i in range(1, len(times)):
        gap = times[i] - times[i - 1]
        # If the gap is large, assume a new track (completely naive approach).
        if gap > threshold:
            current_track += 1
        track_assignments[i] = current_track

    return track_assignments

def advanced_deinterleave(times: np.ndarray, other_data: np.ndarray) -> np.ndarray:
    """
    Placeholder for a more sophisticated approach. Could analyze PRI patterns,
    amplitude, or frequency. Possibly cluster pulses via K-means or DBSCAN.

    Args:
        times (np.array): Sorted array of pulse times.
        other_data (np.array): Additional features (amplitude, frequency, etc.).

    Returns:
        track_assignments (np.array): An array of track indices for each pulse.
    """
    # This might involve:
    # 1. Estimate repeating intervals (PRIs).
    # 2. Group pulses that share similar intervals.
    # 3. Possibly combine amplitude/frequency to refine grouping.

    # For now, we just return a single track (placeholder).
    return np.zeros_like(times, dtype=int)

def main():
    parser = argparse.ArgumentParser(description="Deinterleave pulses from a CSV file.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input CSV file.")
    parser.add_argument("--method", type=str, default="naive", choices=["naive", "advanced"],
                        help="Which deinterleaving method to use.")
    parser.add_argument("--threshold", type=float, default=0.02,
                        help="Time gap threshold for naive method.")
    args = parser.parse_args()

    # Load data
    df = load_pulses(args.input)
    times = df["time"].values
    amps = df["amplitude"].values

    # Perform deinterleaving
    if args.method == "naive":
        track_assignments = simple_time_based_deinterleave(times, threshold=args.threshold)
    else:
        # placeholder approach
        other_data = np.column_stack((amps,))  # add amplitude as extra feature
        track_assignments = advanced_deinterleave(times, other_data)

    # Print basic info
    num_tracks = len(np.unique(track_assignments))
    print(f"Identified {num_tracks} track(s) using method '{args.method}'.")

    # Optionally: create a new DataFrame with track labels
    df["track_id"] = track_assignments

    # Show final track distribution
    track_counts = df["track_id"].value_counts().sort_index()
    print("\nPulse counts per track:\n", track_counts)
    print("\nFirst few rows:\n", df.head())

    # Plot results
    plot_deinterleaved_tracks(track_assignments, times, amps)

if __name__ == "__main__":
    main()
