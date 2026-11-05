import csv
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
    ConfusionMatrixDisplay
)

from motor_fault_simulator import generate_motor_data
from fault_classifier import extract_features, classify_fault


CONDITIONS = [
    "NORMAL",
    "IMBALANCE",
    "MISALIGNMENT",
    "BEARING FAULT"
]

SAMPLES_PER_CLASS = 200


def generate_dataset():

    features = []
    labels = []

    np.random.seed(42)

    for condition in CONDITIONS:

        for _ in range(SAMPLES_PER_CLASS):

            _, signal, _, _, _ = generate_motor_data(condition)

            extracted = extract_features(signal)

            features.append(extracted)
            labels.append(condition)

    return np.array(features), np.array(labels)


def evaluate_model(name, actual, predicted):

    accuracy = accuracy_score(actual, predicted)

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            actual,
            predicted,
            labels=CONDITIONS,
            average="macro",
            zero_division=0
        )
    )

    print("\n====================================")
    print(name)
    print("====================================")

    print("Accuracy:", round(accuracy * 100, 2), "%")
    print("Macro Precision:", round(precision * 100, 2), "%")
    print("Macro Recall:", round(recall * 100, 2), "%")
    print("Macro F1-score:", round(f1 * 100, 2), "%")

    print("\nClassification Report:")

    print(
        classification_report(
            actual,
            predicted,
            labels=CONDITIONS,
            zero_division=0
        )
    )

    return {
        "Model": name,
        "Accuracy": accuracy * 100,
        "Macro Precision": precision * 100,
        "Macro Recall": recall * 100,
        "Macro F1": f1 * 100
    }


def save_confusion_matrix(actual, predicted):

    matrix = confusion_matrix(
        actual,
        predicted,
        labels=CONDITIONS
    )

    display = ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=CONDITIONS
    )

    fig, ax = plt.subplots(figsize=(9, 7))

    display.plot(
        ax=ax,
        cmap="Blues",
        values_format="d"
    )

    plt.title("EdgeGuard Random Forest Confusion Matrix")
    plt.xticks(rotation=20)
    plt.tight_layout()

    plt.savefig("ml_confusion_matrix.png", dpi=300)

    plt.close(fig)

    print("\nSaved: ml_confusion_matrix.png")


def save_comparison(results):

    with open(
        "model_comparison.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Model",
                "Accuracy",
                "Macro Precision",
                "Macro Recall",
                "Macro F1"
            ]
        )

        writer.writeheader()

        for result in results:
            writer.writerow(result)

    print("Saved: model_comparison.csv")


def main():

    print("\n====================================")
    print(" EDGEGUARD MACHINE LEARNING")
    print(" RANDOM FOREST CLASSIFIER")
    print("====================================")

    print("\nGenerating synthetic vibration dataset...")

    X, y = generate_dataset()

    print("Total samples:", len(X))
    print("Features per sample:", X.shape[1])
    print("Samples per fault category:", SAMPLES_PER_CLASS)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\nTraining samples:", len(X_train))
    print("Testing samples:", len(X_test))

    print("\nTraining Random Forest model...")

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    ml_predictions = model.predict(X_test)

    print("\nRandom Forest training completed!")

    rule_predictions = []

    for row in X_test:

        rms, peak, std_dev, crest, harmonic_ratio = row

        prediction = classify_fault(
            rms,
            peak,
            crest,
            harmonic_ratio
        )

        rule_predictions.append(prediction)

    print("\nEvaluating both classifiers...")

    rule_results = evaluate_model(
        "RULE-BASED CLASSIFIER",
        y_test,
        rule_predictions
    )

    ml_results = evaluate_model(
        "RANDOM FOREST CLASSIFIER",
        y_test,
        ml_predictions
    )

    print("\n====================================")
    print(" MODEL PERFORMANCE COMPARISON")
    print("====================================")

    print(
        f"{'Metric':<22}"
        f"{'Rule-Based':>15}"
        f"{'Random Forest':>18}"
    )

    metrics = [
        ("Accuracy", "Accuracy"),
        ("Macro Precision", "Macro Precision"),
        ("Macro Recall", "Macro Recall"),
        ("Macro F1", "Macro F1")
    ]

    for label, key in metrics:

        print(
            f"{label:<22}"
            f"{rule_results[key]:>14.2f}%"
            f"{ml_results[key]:>17.2f}%"
        )

    save_confusion_matrix(y_test, ml_predictions)

    save_comparison([
        rule_results,
        ml_results
    ])

    print("\n====================================")
    print(" ML EVALUATION COMPLETED")
    print("====================================")


if __name__ == "__main__":
    main()