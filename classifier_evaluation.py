import numpy as np
import matplotlib.pyplot as plt
import csv

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

    # Reproducible evaluation
    np.random.seed(42)

    confusion_matrix = np.zeros((4, 4), dtype=int)

    correct = 0
    total = 0

    print("\n======================================")
    print(" EDGEGUARD CLASSIFIER EVALUATION")
    print("======================================")

    # Generate and classify test samples
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

    accuracy = correct / total

    print("\nTotal samples tested:", total)
    print("Correct predictions:", correct)
    print("Incorrect predictions:", total - correct)
    print("Classification accuracy:", round(accuracy * 100, 2), "%")

    # Calculate precision, recall and F1-score
    class_results = []

    print("\nCLASSIFICATION METRICS")
    print("-" * 65)

    for i, condition in enumerate(conditions):

        true_positive = confusion_matrix[i, i]

        false_positive = (
            np.sum(confusion_matrix[:, i]) - true_positive
        )

        false_negative = (
            np.sum(confusion_matrix[i, :]) - true_positive
        )

        support = np.sum(confusion_matrix[i, :])

        precision = (
            true_positive / (true_positive + false_positive)
            if (true_positive + false_positive) > 0 else 0
        )

        recall = (
            true_positive / (true_positive + false_negative)
            if (true_positive + false_negative) > 0 else 0
        )

        f1_score = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0 else 0
        )

        class_results.append({
            "class": condition,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "support": support
        })

        print("\n", condition)
        print("Precision:", round(precision * 100, 2), "%")
        print("Recall:", round(recall * 100, 2), "%")
        print("F1-score:", round(f1_score * 100, 2), "%")

    # Macro averages
    macro_precision = np.mean(
        [result["precision"] for result in class_results]
    )

    macro_recall = np.mean(
        [result["recall"] for result in class_results]
    )

    macro_f1 = np.mean(
        [result["f1_score"] for result in class_results]
    )

    print("\n======================================")
    print(" OVERALL METRICS")
    print("======================================")

    print("Accuracy:", round(accuracy * 100, 2), "%")
    print("Macro Precision:", round(macro_precision * 100, 2), "%")
    print("Macro Recall:", round(macro_recall * 100, 2), "%")
    print("Macro F1-score:", round(macro_f1 * 100, 2), "%")

    # Save evaluation results to CSV
    with open("evaluation_results.csv", "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "class",
                "precision",
                "recall",
                "f1_score",
                "support",
                "accuracy"
            ]
        )

        writer.writeheader()

        for result in class_results:

            writer.writerow({
                **result,
                "accuracy": ""
            })

        writer.writerow({
            "class": "MACRO AVERAGE",
            "precision": macro_precision,
            "recall": macro_recall,
            "f1_score": macro_f1,
            "support": total,
            "accuracy": accuracy
        })

    # Display and save confusion matrix
    print("\nCONFUSION MATRIX")
    print("Rows = Actual | Columns = Predicted")
    print("\n", confusion_matrix)

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

    plt.savefig("confusion_matrix.png", dpi=300)

    print("\n======================================")
    print(" EVALUATION FILES SAVED")
    print("======================================")

    print("1. evaluation_results.csv")
    print("2. confusion_matrix.png")

    plt.show()
    plt.close()

    return confusion_matrix, accuracy * 100


if __name__ == "__main__":
    run_evaluation()