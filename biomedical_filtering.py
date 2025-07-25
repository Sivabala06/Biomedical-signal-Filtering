"""
Signal Filtering and Visualization Tool for ECG/EEG

This script:
- Loads signal data from CSV/Excel files
- Estimates sampling frequency from timestamps
- Applies a bandpass filter suitable for ECG or EEG
- Plots original and filtered signals
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import os

# ----------------------------
# Load signal data from file
# ----------------------------
def load_data(file_path):
    """
    Load time-series signal data (ECG/EEG) from CSV or Excel file.

    Args:
        file_path (str): Path to the .csv or .xlsx file

    Returns:
        DataFrame with columns: ['Time', 'Signal', 'Time_sec']
    """
    # Read based on file type
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, skiprows=2)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, skiprows=2)
    else:
        raise ValueError("Unsupported file type. Use .csv or .xlsx only.")

    # Standardize column names
    df.columns = ['Time', 'Signal']

    # Remove stray quotes and normalize time format
    df['Time'] = df['Time'].astype(str).str.replace("'", "", regex=False)
    df['Time'] = df['Time'].apply(lambda x: '00:' + x if x.count(':') == 1 else x)

    # Convert time to seconds
    df['Time_sec'] = pd.to_timedelta(df['Time']).dt.total_seconds()

    # Convert signal to numeric values
    df['Signal'] = pd.to_numeric(df['Signal'], errors='coerce')
    df.dropna(subset=['Signal'], inplace=True)

    return df

# ----------------------------
# Apply bandpass filter
# ----------------------------
def filter_signal(data, fs, signal_type, order=4):
    """
    Apply a bandpass Butterworth filter to the input signal.

    Args:
        data (array-like): Raw signal values
        fs (int): Sampling frequency in Hz
        signal_type (str): 'ecg' or 'eeg'
        order (int): Filter order (default=4)

    Returns:
        Filtered signal as numpy array
    """
    nyq = 0.5 * fs

    if signal_type == 'ecg':
        lowcut = 0.5
        highcut = 45.0
    elif signal_type == 'eeg':
        lowcut = 1.0  # safer for EEG
        highcut = 30.0
    else:
        raise ValueError("Unsupported signal type. Choose 'ecg' or 'eeg'.")

    low = lowcut / nyq
    high = highcut / nyq

    if not (0 < low < high < 1):
        raise ValueError(f"Invalid filter range. fs={fs}, low={lowcut}, high={highcut}")

    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# ----------------------------
# Main function
# ----------------------------
def main():
    """
    Executes the full signal processing pipeline:
    - Load signal
    - Estimate sampling frequency
    - Filter signal
    - Plot results
    """
    # User input
    file_path = input("Enter path to ECG/EEG file (.csv or .xlsx): ")
    signal_type = input("Enter signal type (ECG or EEG): ").strip().lower()

    if not os.path.exists(file_path):
        print("File not found.")
        return

    # Load data
    df = load_data(file_path)

    # Estimate sampling frequency
    time_diffs = np.diff(df['Time_sec'])
    fs = round(1 / np.mean(time_diffs))
    print(f"Estimated sampling frequency: {fs} Hz")

    # Filter the signal
    filtered_signal = filter_signal(df['Signal'], fs, signal_type)

    # Plot original and filtered signal
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(df['Time_sec'], df['Signal'], color='gray')
    plt.title(f"{signal_type.upper()} Signal - Original")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(df['Time_sec'], filtered_signal, color='blue')
    plt.title(f"{signal_type.upper()} Signal - Filtered")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # Optional: Save filtered data
    save_option = input("Save filtered signal as CSV? (y/n): ").strip().lower()
    if save_option == 'y':
        df['Filtered_Signal'] = filtered_signal
        output_file = 'filtered_output.csv'
        df.to_csv(output_file, index=False)
        print(f"Filtered signal saved to: {output_file}")

# ----------------------------
# Script entry point
# ----------------------------
if __name__ == "__main__":
    main()
