import csv
import numpy as np
import matplotlib.pyplot as plt

from motor_fault_simulator import SAMPLE_COUNT
from fault_classifier import extract_features, classify_fault
from sklearn.ensemble import RandomForestClassifier


CONDITIONS = [
    "NORMAL",
    "IMBALANCE",
    "MISALIGNMENT",
    "BEARING FAULT"
]

AMPLITUDE_LEVELS = [0.8, 1.0, 1.2]
NOISE_LEVELS = [0.005, 0.02, 0.04]

TRAINING_SAMPLES_PER_CLASS = 300
TEST_REPEATS = 30


def generate_variable_signal(
    condition,
    amplitude_scale=1.0,
    noise_std=0.005
):

    t = np.arange(SAMPLE_COUNT) / 100

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

        for i in range(0, SAMPLE_COUNT, 20):
            signal[i] += 0.30

    else:
        raise ValueError("Unknown motor condition")

    signal = amplitude_scale * signal

    noise = np.random.normal(
        0,
        noise_std,
        SAMPLE_COUNT
    )

    return signal + noise


def extract_signal_features(signal):
    return extract_features(signal)


def generate_training_dataset():

    features = []
    labels = []

    for condition in CONDITIONS:

        for _ in range(TRAINING_SAMPLES_PER_CLASS):

            amplitude = np.random.uniform(0.8, 1.2)
            noise = np.random.uniform(0.005, 0.04)

            signal = generate_variable_signal(
                condition,
                amplitude,
                noise
            )

            features.append(
                extract_signal_features(signal)
            )

            labels.append(condition)

    return np.array(features), np.array(labels)


def train_random_forest():

    print("\nGenerating varied training dataset...")

    X_train, y_train = generate_training_dataset()

    print("Training samples:", len(X_train))

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    print("Random Forest training completed!")

    return model


def evaluate_robustness(model):

    results = []

    print("\n========================================")
    print(" EDGEGUARD ROBUSTNESS TEST")
    print("========================================")

    for amplitude in AMPLITUDE_LEVELS:

        for noise in NOISE_LEVELS:

            rule_correct = 0
            ml_correct = 0
            total = 0

            for condition in CONDITIONS:

                for _ in range(TEST_REPEATS):

                    signal = generate_variable_signal(
                        condition,
                        amplitude,
                        noise
                    )

                    features = extract_signal_features(signal)

                    rms, peak, std_dev, crest, harmonic_ratio = (
                        features
                    )

                    rule_prediction = classify_fault(
                        rms,
                        peak,
                        crest,
                        harmonic_ratio
                    )

                    ml_prediction = model.predict(
                        np.array(features).reshape(1, -1)
                    )[0]

                    if rule_prediction == condition:
                        rule_correct += 1

                    if ml_prediction == condition:
                        ml_correct += 1

                    total += 1

            rule_accuracy = rule_correct / total * 100
            ml_accuracy = ml_correct / total * 100

            result = {
                "Amplitude Scale": amplitude,
                "Noise Standard Deviation": noise,
                "Rule-Based Accuracy": round(rule_accuracy, 2),
                "Random Forest Accuracy": round(ml_accuracy, 2),
                "Total Test Samples": total
            }

            results.append(result)

            print(
                f"\nAmplitude: {amplitude}x | "
                f"Noise: {noise} g"
            )

            print(
                f"Rule-Based Accuracy: {rule_accuracy:.2f}%"
            )

            print(
                f"Random Forest Accuracy: {ml_accuracy:.2f}%"
            )

    return results


def save_results(results):

    with open(
        "robustness_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Amplitude Scale",
                "Noise Standard Deviation",
                "Rule-Based Accuracy",
                "Random Forest Accuracy",
                "Total Test Samples"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print("\nSaved: robustness_results.csv")


def save_comparison_chart(results):

    labels = [
        f"{item['Amplitude Scale']}x\n"
        f"{item['Noise Standard Deviation']}g"
        for item in results
    ]

    rule_values = [
        item["Rule-Based Accuracy"]
        for item in results
    ]

    ml_values = [
        item["Random Forest Accuracy"]
        for item in results
    ]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(13, 6))

    ax.bar(
        x - width / 2,
        rule_values,
        width,
        label="Rule-Based"
    )

    ax.bar(
        x + width / 2,
        ml_values,
        width,
        label="Random Forest"
    )

    ax.set_xlabel("Amplitude and Noise Conditions")
    ax.set_ylabel("Classification Accuracy (%)")
    ax.set_title("EdgeGuard Robustness Performance Comparison")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        "robustness_comparison.png",
        dpi=300
    )

    plt.close(fig)

    print("Saved: robustness_comparison.png")


def main():

    np.random.seed(42)

    model = train_random_forest()

    results = evaluate_robustness(model)

    save_results(results)

    save_comparison_chart(results)

    print("\n========================================")
    print(" ROBUSTNESS EXPERIMENT COMPLETED")
    print("========================================")


if __name__ == "__main__":
    main()