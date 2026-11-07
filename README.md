# EdgeGuard â€“ Motor Fault Detection and Monitoring System

[![EdgeGuard CI](https://github.com/Sharonhoney05/EdgeGuard/actions/workflows/tests.yml/badge.svg)](https://github.com/Sharonhoney05/EdgeGuard/actions/workflows/tests.yml)

> **Simulation Disclaimer:** All results in this project are generated using simulated motor vibration signals. The system has not been validated using measurements from real motors.

EdgeGuard is a Python-based motor condition monitoring prototype that analyzes vibration signals to classify four operating conditions: Normal, Imbalance, Misalignment, and Bearing Fault.

It combines signal generation, feature extraction, rule-based classification, machine learning, robustness evaluation, dashboards, database storage, reporting, and automated testing.

## 1. Key Features

- Synthetic motor vibration signal generation.
- Statistical and frequency-domain feature extraction.
- Threshold-based rule classifier.
- Random Forest machine learning classifier.
- Five-fold stratified cross-validation.
- Feature importance analysis.
- Stress testing with additional noise and amplitude variation.
- Interactive Tkinter monitoring dashboards.
- SQLite monitoring history.
- CSV and PDF report generation.
- Automated testing with pytest.
- GitHub Actions continuous integration.

## 2. System Workflow

1. Generate synthetic vibration signals for four motor conditions.
2. Extract five signal features: RMS, peak amplitude, standard deviation, crest factor, and harmonic ratio.
3. Classify signals using rule-based logic and a Random Forest model.
4. Evaluate models using held-out test data and cross-validation.
5. Run a separate stress test using additional noise and amplitude variation.
6. Display monitoring results and history through the dashboard.
7. Export monitoring information to CSV and PDF reports.

## 3. Classification Methods

3.1 Rule-Based Classifier

The rule-based classifier uses predefined thresholds based on the characteristics of the simulated signals.

Features used:

- RMS
- Peak amplitude
- Crest factor
- Harmonic ratio

Current decision rules:

Condition| Rule
Bearing Fault| Peak amplitude > 0.25 and crest factor > 2.5
Misalignment| Harmonic ratio > 0.4
Imbalance| RMS > 0.05
Normal| None of the above conditions

These thresholds are specific to the current synthetic signal patterns. They are experimental project parameters, not universal industrial diagnostic limits.

3.2 Random Forest Classifier

The Random Forest model uses all five extracted features:

- RMS
- Peak amplitude
- Standard deviation
- Crest factor
- Harmonic ratio

Model Configuration

Parameter| Configuration
Algorithm| Random Forest
Number of estimators| 200
Dataset size| 800 synthetic samples
Training samples| 640
Baseline test samples| 160
Train/test split| 80:20, stratified
Random state| 42
Class weighting| Balanced

## 4. Baseline Evaluation and Cross-Validation

The baseline dataset contains 800 synthetic samples, with 200 samples per motor condition.

The held-out test set contains 160 samples, with 40 samples per condition.

Evaluation| Result
Rule-Based Test Accuracy| 100%
Random Forest Test Accuracy| 100%
Five-Fold Mean CV Accuracy| 100%
CV Standard Deviation| 0%

The five-fold stratified cross-validation is performed on the training portion of the synthetic dataset.

Interpretation: The perfect baseline scores reflect the clearly separated patterns used by this simulator. They do not establish real-world diagnostic accuracy. The stress test below provides a more challenging evaluation of the trained Random Forest model.

## 5. Feature Importance

The Random Forest model produced the following impurity-based feature importance scores:

Feature| Importance
Crest Factor| 23.57%
Standard Deviation| 22.47%
RMS| 21.27%
Harmonic Ratio| 18.47%
Peak Amplitude| 14.22%

"Random Forest Feature Importance" (results/feature_importance.png)

These scores describe how the trained model used the features to split its training data. They do not establish causal relationships.

## 6. Robustness and Stress Testing

A separate stress dataset was generated to evaluate both classifiers under more challenging simulated conditions.

Stress-Test Configuration

- 400 additional samples: 100 per motor condition.
- Additional Gaussian noise with standard deviation 0.02.
- Random amplitude scaling between 0.8x and 1.2x.
- Both classifiers evaluated on the same test samples.
- Random Forest trained on the baseline dataset.

Stress-Test Results

Metric| Rule-Based| Random Forest
Accuracy| 100.00%| 85.00%
Macro Precision| 100.00%| 85.10%
Macro Recall| 100.00%| 85.00%
Macro F1-Score| 100.00%| 84.96%

Class-Wise Recall (Random Forest)

Condition| Recall
Normal| 100%
Imbalance| 75%
Misalignment| 65%
Bearing Fault| 100%

"Stress Test Accuracy Comparison" (results/stress_test_comparison.png)

"Random Forest Stress Test Confusion Matrix" (results/stress_confusion_matrix.png)

"Rule-Based Stress Test Confusion Matrix" (results/stress_rule_confusion_matrix.png)

The Rule-Based classifier achieved 100% accuracy on this synthetic stress dataset, while Random Forest achieved 85%. The rule-based thresholds are designed around the simulated fault patterns, so this result does not establish superior real-world performance.

The Random Forest model had difficulty distinguishing Imbalance and Misalignment under additional noise and amplitude variation.

These results identify limitations and differences in the current synthetic experiment rather than proving performance on physical motors.

## 7. Application Screenshots

7.1 Motor Condition Detection

Normal Condition

"Normal Motor Condition" (screenshots/normal.png)

Imbalance Detection

"Imbalance Detection" (screenshots/imbalance.png)

Misalignment Detection

"Misalignment Detection" (screenshots/misalignment.png)

Bearing Fault Detection

"Bearing Fault Detection" (screenshots/bearing_fault.png)

7.2 Monitoring Dashboard and History

Analytics Dashboard

"Analytics Dashboard" (screenshots/analytics.png)

Monitoring History

"Monitoring History" (screenshots/view_history.png)

Detailed Monitoring History

"Detailed Monitoring History" (screenshots/view_history_details.png)

## 8. Technology Stack

Technology| Purpose
Python 3.12+| Core application development environment
NumPy| Signal generation and numerical calculations
Matplotlib| Charts, plots, and confusion matrices
scikit-learn| Random Forest and model evaluation
Tkinter| Desktop dashboard interface
SQLite| Monitoring history storage
ReportLab| PDF report generation
pytest| Automated testing
GitHub Actions| Continuous integration

## 9. Installation and Setup

Prerequisites: Python 3.12 or later and Git.

Step 1: Clone the Repository

git clone https://github.com/Sharonhoney05/EdgeGuard.git

Step 2: Navigate into the Project

cd EdgeGuard

Step 3: Install Dependencies

python -m pip install -r requirements.txt

## 10. Running the Project

Run the integrated monitoring dashboard:

python edgeguard_integrated_dashboard.py

Run the Random Forest evaluation, including cross-validation and stress testing:

python edgeguard_ml_classifier.py

Run the standalone rule-based evaluation:

python classifier_evaluation.py

Run the separate robustness experiment:

python edgeguard_robustness_test.py

## 11. Automated Testing and Continuous Integration

Run the complete local test suite:

python -m pytest -q

Latest verified local result: 27 passed.

GitHub Actions CI

GitHub Actions automatically runs the complete pytest suite:

- On pushes to the "main" branch.
- On pull requests targeting "main".
- Using an Ubuntu environment.
- Using Python 3.12+.
- Installing dependencies from "requirements.txt".

"View GitHub Actions Runs" (https://github.com/Sharonhoney05/EdgeGuard/actions)

## 12. Project Structure

EdgeGuard/
â”œâ”€â”€ .github/
â”‚   â””â”€â”€ workflows/
â”‚       â””â”€â”€ tests.yml
â”œâ”€â”€ examples/
â”‚   â””â”€â”€ vibration_basics.py
â”œâ”€â”€ results/
â”‚   â”œâ”€â”€ confusion_matrix.png
â”‚   â”œâ”€â”€ cross_validation_results.csv
â”‚   â”œâ”€â”€ edgeguard_monitoring_report.csv
â”‚   â”œâ”€â”€ EdgeGuard_Monitoring_Report.pdf
â”‚   â”œâ”€â”€ evaluation_results.csv
â”‚   â”œâ”€â”€ feature_importance.png
â”‚   â”œâ”€â”€ ml_confusion_matrix.png
â”‚   â”œâ”€â”€ model_comparison.csv
â”‚   â”œâ”€â”€ robustness_comparison.png
â”‚   â”œâ”€â”€ robustness_results.csv
â”‚   â”œâ”€â”€ stress_confusion_matrix.png
â”‚   â”œâ”€â”€ stress_rule_confusion_matrix.png
â”‚   â”œâ”€â”€ stress_test_comparison.png
â”‚   â””â”€â”€ stress_test_results.csv
â”œâ”€â”€ screenshots/
â”œâ”€â”€ classifier_evaluation.py
â”œâ”€â”€ edgeguard_database.py
â”œâ”€â”€ edgeguard_export.py
â”œâ”€â”€ edgeguard_integrated_dashboard.py
â”œâ”€â”€ edgeguard_ml_classifier.py
â”œâ”€â”€ edgeguard_pdf_report.py
â”œâ”€â”€ edgeguard_robustness_test.py
â”œâ”€â”€ edgeguard_dashboard.py
â”œâ”€â”€ fault_classifier.py
â”œâ”€â”€ fault_visualization.py
â”œâ”€â”€ motor_fault_simulator.py
â”œâ”€â”€ test_edgeguard.py
â”œâ”€â”€ LICENSE
â”œâ”€â”€ README.md
â”œâ”€â”€ requirements.txt
â””â”€â”€ .gitignore

Note: "edgeguard_dashboard.py" is a standalone dashboard that generates simulated three-axis vibration data and displays vibration measurements and motor condition classifications.

## 13. Limitations and Future Improvements

Current Limitations

- The current project uses synthetic signals and has not been validated against real motor sensor data.
- Rule-based thresholds are specific to the simulator and require calibration for real equipment.
- Stress testing shows confusion between Imbalance and Misalignment under more challenging simulated conditions.
- Current experiments do not establish performance across different physical motors, speeds, loads, or sensor placements.

Future Improvements

- Evaluate using publicly available real motor vibration datasets.
- Collect measurements using physical vibration sensors.
- Improve classification between similar fault conditions.
- Evaluate performance across different motor speeds and operating loads.
- Develop real-time sensor-based monitoring and alerts.

## 14. Author

F K Sharon

Electronics and Communication Engineering
BITM Ballari | 2027

Project: EdgeGuard â€“ Motor Fault Detection and Monitoring System

"GitHub Repository" (https://github.com/Sharonhoney05/EdgeGuard)

Project Disclaimer

EdgeGuard is an academic simulation-based prototype developed for learning and experimentation in vibration analysis, motor condition monitoring, machine learning, and software-based fault detection.

Reported metrics are from synthetic experiments and should not be interpreted as validated industrial diagnostic performance.

License

This project is licensed under the MIT License. See the "LICENSE" (LICENSE) file for details.
