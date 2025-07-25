# Biomedical Signal Filtering using Python

This project focuses on filtering noisy biomedical signals (ECG and EEG) using a 4th-order Butterworth Bandpass Filter. It demonstrates how to clean real-world physiological data by removing noise like baseline drift in EEG and high-frequency interference in ECG.

## Project Overview
Biomedical signals are often contaminated by various types of noise due to muscle movements, electrode shifts, and electrical interference. This project aims to:

- Import time-series biomedical data (CSV/XLSX)
- Calculate sampling frequency from timestamps
- Apply bandpass filtering using `scipy.signal.butter` and `filtfilt`
- Visualize and compare original vs. filtered signals

## 🛠 Tools & Libraries
**Python 3.x**
   - pandas – for data handling
   - numpy – for numerical operations
   - matplotlib – for plotting signals
   - scipy.signal – for digital filtering

## ⚙️ Filtering Details

| Signal Type | Frequency Band (Hz) | Noise Removed               |

|   ECG       | 0.5 – 45 Hz         | High-frequency noise        |
|   EEG       | 1 – 30 Hz           | Baseline drift & low-freq.  |


##  Screenshots
-  EEG with baseline drift (Before & After filtering)
-  ECG with high-frequency noise (Before & After filtering)

## Report
Included: A handwritten report explaining the method, objectives, and signal processing approach — ideal for students and beginners in biomedical engineering.

## Future Work
- Extend filtering to EMG signals  
- Add GUI using `Tkinter` or `Streamlit`  
- Implement frequency spectrum analysis (FFT)


