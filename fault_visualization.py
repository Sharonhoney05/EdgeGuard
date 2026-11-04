import numpy as np
import matplotlib.pyplot as plt

from motor_fault_simulator import generate_motor_data

conditions = [
    "NORMAL",
    "IMBALANCE",
    "MISALIGNMENT",
    "BEARING FAULT"
]

fig, axes = plt.subplots(4, 2, figsize=(13, 14))

fig.suptitle(
    "EDGEGUARD - MOTOR FAULT VISUALIZATION\n"
    "SIMULATED DATA - NOT REAL SENSOR MEASUREMENTS",
    fontsize=14,
    fontweight="bold"
)

for i, condition in enumerate(conditions):

    t, signal, rms, peak, std_dev = generate_motor_data(condition)

    # Time-domain vibration graph
    axes[i, 0].plot(t, signal)
    axes[i, 0].set_title(condition + " - Vibration Signal")
    axes[i, 0].set_xlabel("Time (seconds)")
    axes[i, 0].set_ylabel("Acceleration (g)")
    axes[i, 0].grid(True)

    # Frequency-domain FFT graph
    frequencies = np.fft.rfftfreq(len(signal), d=0.01)
    spectrum = np.abs(np.fft.rfft(signal))

    axes[i, 1].plot(frequencies, spectrum)
    axes[i, 1].set_xlim(0, 25)
    axes[i, 1].set_title(condition + " - Frequency Spectrum")
    axes[i, 1].set_xlabel("Frequency (Hz)")
    axes[i, 1].set_ylabel("FFT Amplitude")
    axes[i, 1].grid(True)

plt.tight_layout()
plt.show()