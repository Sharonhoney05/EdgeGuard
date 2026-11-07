import csv
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score
)
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

FEATURE_NAMES = [
    "RMS",
    "Peak Amplitude",
    "Standard Deviation",
    "Crest Factor",
    "Harmonic Ratio"
]

SAMPLES_PER_CLASS = 200
STRESS_SAMPLES_PER_CLASS = 100


def generate_dataset(
    samples_per_class=SAMPLES_PER_CLASS,
    extra_noise_std=0.0,
    amplitude_range=None
):

    features = []
    labels = []

    for condition in CONDITIONS:

        for _ in range(samples_per_class):

            _, signal, _, _, _ = generate_motor_data(condition)

            # Optional amplitude variation
            if amplitude_range is not None:

                scale = np.random.uniform(
                    amplitude_range[0],
                    amplitude_range[1]
                )

                signal = signal * scale

            # Optional additional test noise
            if extra_noise_std > 0:

                additional_noise = np.random.normal(
                    0,
                    extra_noise_std,
                    len(signal)
                )

                signal = signal + additional_noise

            extracted = extract_features(signal)

            features.append(extracted)
            labels.append(condition)

    return np.array(features), np.array(labels)


def create_model():

    return RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )


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
    print("Macro F1:", round(f1 * 100, 2), "%")

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


def save_confusion_matrix(
    actual,
    predicted,
    filename="ml_confusion_matrix.png",
    title="EdgeGuard Random Forest Confusion Matrix"
):

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

    plt.title(title)
    plt.xticks(rotation=20)
    plt.tight_layout()

    plt.savefig(filename, dpi=300)
    plt.close(fig)

    print("Saved:", filename)


def save_feature_importance(model):

    importance = model.feature_importances_

    indices = np.argsort(importance)

    plt.figure(figsize=(9, 6))

    plt.barh(
        np.array(FEATURE_NAMES)[indices],
        importance[indices]
    )

    plt.xlabel("Feature Importance")
    plt.ylabel("Vibration Features")
    plt.title("EdgeGuard - Random Forest Feature Importance")

    plt.tight_layout()
    plt.savefig("feature_importance.png", dpi=300)
    plt.close()

    print("Saved: feature_importance.png")

    print("\nFEATURE IMPORTANCE")

    for index in np.argsort(importance)[::-1]:

        print(
            FEATURE_NAMES[index],
            ":",
            round(importance[index], 4)
        )


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
        writer.writerows(results)

    print("Saved: model_comparison.csv")


def save_cv_results(scores):

    with open(
        "cross_validation_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Fold",
            "Accuracy"
        ])

        for fold, score in enumerate(scores, start=1):

            writer.writerow([
                fold,
                score * 100
            ])

    print("Saved: cross_validation_results.csv")


def main():

    print("\n====================================")
    print(" EDGEGUARD MACHINE LEARNING")
    print(" RANDOM FOREST CLASSIFIER")
    print("====================================")

    # ---------------------------------
    # BASELINE DATASET
    # ---------------------------------

    print("\nGenerating baseline synthetic dataset...")

    np.random.seed(42)

    X, y = generate_dataset()

    print("Total samples:", len(X))
    print("Features per sample:", X.shape[1])
    print("Samples per category:", SAMPLES_PER_CLASS)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\nTraining samples:", len(X_train))
    print("Testing samples:", len(X_test))

    # ---------------------------------
    # FIVE-FOLD CROSS VALIDATION
    # ---------------------------------

    print("\n====================================")
    print(" 5-FOLD CROSS VALIDATION")
    print("====================================")

    model = create_model()

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    cv_scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="accuracy"
    )

    print("\nFold Accuracy:")

    for fold, score in enumerate(cv_scores, start=1):

        print(
            f"Fold {fold}: {score * 100:.2f}%"
        )

    print(
        "\nMean CV Accuracy:",
        round(np.mean(cv_scores) * 100, 2),
        "%"
    )

    print(
        "CV Standard Deviation:",
        round(np.std(cv_scores) * 100, 2),
        "%"
    )

    save_cv_results(cv_scores)

    # ---------------------------------
    # FINAL MODEL TRAINING
    # ---------------------------------

    print("\nTraining Random Forest model...")

    model.fit(X_train, y_train)

    ml_predictions = model.predict(X_test)

    print("\nRandom Forest training completed!")

    # ---------------------------------
    # RULE-BASED CLASSIFIER
    # ---------------------------------

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

    print("\n====================================")
    print(" BASELINE MODEL EVALUATION")
    print("====================================")

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

    save_confusion_matrix(
        y_test,
        ml_predictions
    )

    save_feature_importance(model)

    save_comparison([
        rule_results,
        ml_results
    ])

    # ---------------------------------
    # NOISY STRESS TEST
    # ---------------------------------

    print("\n====================================")
    print(" RANDOM FOREST STRESS TEST")
    print("====================================")

    print("Additional test noise standard deviation: 0.02")
    print("Original simulator noise standard deviation: 0.005")
    print("Amplitude range: 0.8x to 1.2x")

    np.random.seed(2026)

    X_stress, y_stress = generate_dataset(
        samples_per_class=STRESS_SAMPLES_PER_CLASS,
        extra_noise_std=0.02,
        amplitude_range=(0.8, 1.2)
    )

    stress_predictions = model.predict(X_stress)

    stress_results = evaluate_model(
        "RANDOM FOREST - NOISY STRESS TEST",
        y_stress,
        stress_predictions
    )

    save_confusion_matrix(
        y_stress,
        stress_predictions,
        filename="stress_confusion_matrix.png",
        title="EdgeGuard - Noisy Stress Test"
    )

    with open(
        "stress_test_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=list(stress_results.keys())
        )

        writer.writeheader()
        writer.writerow(stress_results)

    print("Saved: stress_test_results.csv")

    # ---------------------------------
    # FINAL SUMMARY
    # ---------------------------------

    print("\n====================================")
    print(" EDGEGUARD EVALUATION SUMMARY")
    print("====================================")

    print(
        "5-Fold CV Mean:",
        round(np.mean(cv_scores) * 100, 2),
        "%"
    )

    print(
        "Baseline Test Accuracy:",
        round(ml_results["Accuracy"], 2),
        "%"
    )

    print(
        "Noisy Stress Test Accuracy:",
        round(stress_results["Accuracy"], 2),
        "%"
    )

    print("\nAll experiments use synthetic vibration data.")
    print("Results do not establish real-world motor performance.")

    print("\n====================================")
    print(" ML EVALUATION COMPLETED")
    print("====================================")


if __name__ == "__main__":
    main()