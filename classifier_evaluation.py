import numpy as np
import matplotlib.pyplot as plt

from motor_fault_simulator import generate_motor_data
from fault_classifier import extract_features, classify_fault


conditions = [
    "NORMAL",
    "IMBALANCE",
    "MISALIGNMENT",
    "BEARING FAULT"
]

samples_per_condition = 25


def run_evaluation():

    confusion_matrix = np.zeros((4, 4), dtype=int)

    correct = 0
    total = 0

    print("\n======================================")
    print(" EDGEGUARD CLASSIFIER EVALUATION")
    print("======================================")

    for actual_index, actual in enumerate(conditions):

        for sample in range(samples_per_condition):

            t, signal, _, _, _ = generate_motor_data(actual)

            rms, peak, std_dev, crest, harmonic_ratio = (
                extract_features(signal)
            )

            predicted = classify_fault(
                rms, peak, crest, harmonic_ratio
            )

            predicted_index = conditions.index(predicted)

            confusion_matrix[actual_index, predicted_index] += 1

            total += 1

            if actual == predicted:
                correct += 1

    accuracy = (correct / total) * 100

    print("\nTotal samples tested:", total)
    print("Correct predictions:", correct)
    print("Incorrect predictions:", total - correct)
    print("Classification accuracy:", round(accuracy, 2), "%")

    print("\nCONFUSION MATRIX")
    print("Rows = Actual | Columns = Predicted")

    print("\n", confusion_matrix)

    print("\nCLASS-WISE RESULTS")

    for i, condition in enumerate(conditions):

        class_total = np.sum(confusion_matrix[i])
        class_correct = confusion_matrix[i, i]

        class_accuracy = (class_correct / class_total) * 100

        print(condition, ":", round(class_accuracy, 2), "%")

    plt.figure(figsize=(8, 6))

    plt.imshow(confusion_matrix, cmap="Blues")

    plt.title("EdgeGuard - Confusion Matrix")
    plt.xlabel("Predicted Condition")
    plt.ylabel("Actual Condition")

    plt.xticks(range(4), conditions, rotation=20)
    plt.yticks(range(4), conditions)

    for i in range(4):
        for j in range(4):
            plt.text(
                j, i,
                confusion_matrix[i, j],
                ha="center",
                va="center"
            )

    plt.colorbar(label="Number of Samples")
    plt.tight_layout()
    plt.show()

    return confusion_matrix, accuracy


if __name__ == "__main__":
    run_evaluation()