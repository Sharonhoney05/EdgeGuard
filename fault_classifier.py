import numpy as np
from motor_fault_simulator import generate_motor_data


def extract_features(signal):

    rms = float(np.sqrt(np.mean(signal ** 2)))
    peak = float(np.max(np.abs(signal)))
    std_dev = float(np.std(signal))

    crest_factor = peak / rms if rms > 0 else 0

    # Frequency analysis using FFT
    frequencies = np.fft.rfftfreq(len(signal), d=0.01)
    spectrum = np.abs(np.fft.rfft(signal))

    fundamental_index = np.argmin(np.abs(frequencies - 5))
    harmonic_index = np.argmin(np.abs(frequencies - 10))

    fundamental = spectrum[fundamental_index]
    harmonic = spectrum[harmonic_index]

    harmonic_ratio = (
        harmonic / fundamental if fundamental > 0 else 0
    )

    return rms, peak, std_dev, crest_factor, harmonic_ratio


def classify_fault(rms, peak, crest, harmonic_ratio):

    if peak > 0.25 and crest > 2.5:
        return "BEARING FAULT"

    elif harmonic_ratio > 0.4:
        return "MISALIGNMENT"

    elif rms > 0.05:
        return "IMBALANCE"

    else:
        return "NORMAL"


conditions = [
    "NORMAL",
    "IMBALANCE",
    "MISALIGNMENT",
    "BEARING FAULT"
]

correct = 0

print("\n====================================")
print(" EDGEGUARD ADVANCED FAULT CLASSIFIER")
print("====================================")

for actual in conditions:

    t, signal, _, _, _ = generate_motor_data(actual)

    rms, peak, std_dev, crest, harmonic_ratio = (
        extract_features(signal)
    )

    predicted = classify_fault(
        rms, peak, crest, harmonic_ratio
    )

    print("\nActual condition:", actual)
    print("Predicted condition:", predicted)
    print("RMS:", round(rms, 4), "g")
    print("Peak:", round(peak, 4), "g")
    print("Crest factor:", round(crest, 4))
    print("Harmonic ratio:", round(harmonic_ratio, 4))

    if actual == predicted:
        print("Result: CORRECT")
        correct += 1
    else:
        print("Result: INCORRECT")

print("\n====================================")
print("CLASSIFICATION SUMMARY")
print("Correct:", correct, "/", len(conditions))
print("====================================")