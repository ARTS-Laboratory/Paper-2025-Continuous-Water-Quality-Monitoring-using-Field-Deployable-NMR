import subprocess as sp
tmp = sp.call('cls',shell=True)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import detrend

# Load dataset
#file_path = "SPIE7/277070001.csv"  # Update this with the correct file path
file_path = "SPIE4/277000001.csv"

df = pd.read_csv(file_path)


# Extract time and signal data
signal = df["NMR signal (mV)"].values
time = df["time (s)"].values
signal = signal - np.mean(signal)
#signal = detrend(signal)
print(signal)

# Calculate sampling parameters
sampling_time =  time[1]  # Assuming uniform sampling
print (sampling_time)
sampling_rate = 1 / sampling_time
print(sampling_rate)
# Perform FFT
n = len(signal)
fft_values = fft(signal)
freqs = fftfreq(n, sampling_time)

# Plot the FFT spectrum
plt.figure(figsize=(10, 5))
plt.plot(freqs[:n//2], np.abs(fft_values[:n//2]))  # Plot only positive frequencies
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("FFT of the Signal from: "+file_path)
plt.grid()
plt.show()
