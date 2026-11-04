import numpy as np

SAMPLE_COUNT = 1000

def generate_motor_data(condition):
    t = np.arange(SAMPLE_COUNT) / 100

    noise = np.random.normal(0, 0.005, SAMPLE_COUNT)

    if condition == "NORMAL":
        signal = 0.02 * np.sin(2 * np.pi * 5 * t)

    elif condition == "IMBALANCE":
        signal = 0.15 * np.sin(2 * np.pi * 5 * t)

    elif condition == "MISALIGNMENT":
        signal = (
            0.10 * np.sin(2 * np.pi * 5 * t)
            + 0.07 * np.sin(2 * np.pi * 10 * t)
        )

    elif condition == "BEARING FAULT":
        signal = 0.025 * np.sin(2 * np.pi * 5 * t)

        # Simulated repetitive bearing impacts
        for i in range(0, SAMPLE_COUNT, 20):
            signal[i] += 0.30

    else:
        raise ValueError("Unknown motor condition")

    signal = signal + noise

    rms = np.sqrt(np.mean(signal ** 2))
    peak = np.max(np.abs(signal))
    std_dev = np.std(signal)

    return t, signal, rms, peak, std_dev


conditions = [
    "NORMAL",
    "IMBALANCE",
    "MISALIGNMENT",
    "BEARING FAULT"
]

for condition in conditions:
    t, signal, rms, peak, std_dev = generate_motor_data(condition)

    print("\nMotor condition:", condition)
    print("RMS:", round(float(rms), 4), "g")
    print("Peak:", round(float(peak), 4), "g")
    print("Standard deviation:", round(float(std_dev), 4), "g")