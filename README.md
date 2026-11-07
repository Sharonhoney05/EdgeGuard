EdgeGuard – Motor Fault Detection and Monitoring System

"EdgeGuard CI" (https://github.com/Sharonhoney05/EdgeGuard/actions/workflows/tests.yml/badge.svg)

All results in this project are generated using simulated motor vibration data, not measurements from real motors.

EdgeGuard is a Python-based motor fault detection and monitoring system that analyzes vibration signals to identify four operating conditions: Normal, Imbalance, Misalignment, and Bearing Fault.

The project combines signal processing, rule-based classification, machine learning, robustness evaluation, interactive dashboards, and automated testing.

Key Features

- Synthetic motor vibration signal generation using NumPy.
- Statistical and frequency-domain feature extraction.
- Rule-based motor fault classification.
- Random Forest machine learning classifier.
- Five-fold stratified cross-validation.
- Feature importance analysis.
- Noise and amplitude variation stress testing.
- Interactive monitoring and analytics dashboards.
- SQLite-based monitoring history.
- CSV and PDF report generation.
- Automated testing with pytest.
- GitHub Actions continuous integration.

System Architecture

1. Signal Generation: Generates synthetic vibration signals for four motor conditions.
2. Feature Extraction: Calculates RMS, peak amplitude, standard deviation, crest factor, and harmonic ratio.
3. Classification: Uses predefined rules and a Random Forest model to identify motor conditions.
4. Evaluation: Measures accuracy, precision, recall, F1-score, cross-validation performance, and robustness.
5. Monitoring: Displays results through dashboards and stores monitoring history.
6. Reporting: Exports monitoring results into CSV and PDF reports.

Classification Methods

1. Rule-Based Classifier

Uses predefined thresholds based on the characteristics of the simulated vibration signals.

Features used:

- RMS
- Peak amplitude
- Crest factor
- Harmonic ratio

The classifier applies threshold-based conditions to distinguish between normal operation, imbalance, misalignment, and bearing faults.

These thresholds are specific to the simulated dataset and require calibration before any real-world application.

2. Random Forest Classifier

Uses five extracted features:

- RMS
- Peak amplitude
- Standard deviation
- Crest factor
- Harmonic ratio

Model configuration:

- Algorithm: Random Forest
- Number of estimators: 200
- Training/testing split: 80:20
- Stratified data splitting
- Random state: 42
- Class weighting: Balanced

Dataset and Model Evaluation

The baseline synthetic dataset contains 800 samples, with 200 samples for each motor condition.

Evaluation| Result
Total baseline samples| 800
Training samples| 640
Testing samples| 160
Features| 5
Baseline rule-based accuracy| 100%
Baseline Random Forest accuracy| 100%
Five-fold mean CV accuracy| 100%
CV standard deviation| 0%

Important: These baseline results reflect the clearly separated patterns in the synthetic dataset. They should not be interpreted as real-world motor fault detection accuracy.

Feature Importance

The Random Forest model produced the following feature importance scores:

Feature| Importance
Crest Factor| 23.57%
Standard Deviation| 22.47%
RMS| 21.27%
Harmonic Ratio| 18.47%
Peak Amplitude| 14.22%

"Feature Importance" (feature_importance.png)

These scores represent the model's impurity-based feature importance, not causal relationships.

Robustness and Stress Testing

To examine classifier performance under more challenging conditions, a separate stress dataset was generated with:

- Additional Gaussian noise (standard deviation 0.02).
- Random amplitude scaling between 0.8x and 1.2x.
- 400 additional samples, with 100 samples per condition.

The Random Forest model trained on the baseline dataset was evaluated on this stress dataset.

Metric| Stress Test Result
Accuracy| 85.00%
Macro Precision| 85.10%
Macro Recall| 85.00%
Macro F1-score| 84.96%

Class-wise observations

- Normal: 100% recall.
- Bearing Fault: 100% recall.
- Imbalance: 75% recall.
- Misalignment: 65% recall.

The results show that imbalance and misalignment become more difficult to distinguish under additional noise and amplitude variation.

This evaluation highlights the limitations of the current model and provides opportunities for further improvement.

"Stress Test Confusion Matrix" (stress_confusion_matrix.png)

Application Screenshots

Motor Condition Detection

Normal Condition

"Normal" (screenshots/normal.png)

Imbalance Detection

"Imbalance" (screenshots/imbalance.png)

Misalignment Detection

"Misalignment" (screenshots/misalignment.png)

Bearing Fault Detection

"Bearing Fault" (screenshots/bearing_fault.png)

Monitoring Dashboard and History

Analytics Dashboard

"Analytics" (screenshots/analytics.png)

Monitoring History

"Monitoring History" (screenshots/view_history.png)

Detailed History Records

"History Details" (screenshots/view_history_details.png)

Technology Stack

Technology| Purpose
Python 3.12| Core application
NumPy| Signal generation and numerical calculations
Matplotlib| Signal plots, charts, and confusion matrices
Scikit-learn| Random Forest and model evaluation
SQLite| Monitoring history storage
Tkinter| Desktop dashboard interface
ReportLab| PDF report generation
Pytest| Automated testing
GitHub Actions| Continuous integration

Installation and Setup

Prerequisites: Python 3.12 or later and Git.

1. Clone the repository:

git clone https://github.com/Sharonhoney05/EdgeGuard.git

2. Navigate into the project:

cd EdgeGuard

3. Install dependencies:

python -m pip install -r requirements.txt

Running the Project

Run the machine learning evaluation:

python edgeguard_ml_classifier.py

Run the integrated monitoring dashboard:

python edgeguard_integrated_dashboard.py

Run the rule-based evaluation:

python classifier_evaluation.py

Run the robustness evaluation:

python edgeguard_robustness_test.py

Running Automated Tests

Execute the complete test suite:

python -m pytest -q

Latest local test result: 27 passed.

Continuous Integration

GitHub Actions automatically runs the complete pytest suite:

- On pushes to the "main" branch.
- On pull requests targeting the "main" branch.
- Using an Ubuntu environment and Python 3.12.

"View GitHub Actions" (https://github.com/Sharonhoney05/EdgeGuard/actions)

Project Structure

EdgeGuard/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── Day1/
├── screenshots/
│   ├── analytics.png
│   ├── bearing_fault.png
│   ├── imbalance.png
│   ├── misalignment.png
│   ├── normal.png
│   ├── view_history.png
│   └── view_history_details.png
│
├── classifier_evaluation.py
├── confusion_matrix.png
├── cross_validation_results.csv
├── edgeguard_dashboard.py
├── edgeguard_database.py
├── edgeguard_export.py
├── edgeguard_integrated_dashboard.py
├── edgeguard_ml_classifier.py
├── edgeguard_monitoring_report.csv
├── edgeguard_pdf_report.py
├── edgeguard_robustness_test.py
├── EdgeGuard_Monitoring_Report.pdf
├── evaluation_results.csv
├── fault_classifier.py
├── fault_visualization.py
├── feature_importance.png
├── ml_confusion_matrix.png
├── model_comparison.csv
├── motor_fault_simulator.py
├── requirements.txt
├── robustness_comparison.png
├── robustness_results.csv
├── stress_confusion_matrix.png
├── stress_test_results.csv
└── test_edgeguard.py

Limitations and Future Improvements

- Current results are based on synthetic vibration signals rather than real motor sensor measurements.
- Classification thresholds are specific to the simulated signal patterns.
- Imbalance and misalignment performance decreases under noisy conditions.
- Real-world deployment would require validation using actual motor vibration datasets.

Potential future improvements include:

- Testing with real motor vibration datasets.
- Improving classification between similar fault conditions.
- Exploring additional signal-processing features.
- Evaluating performance across different motor speeds and loads.
- Developing a real-time sensor-based monitoring system.

Author

F K Sharon

Electronics and Communication Engineering
BITM Ballari | 2027

Project: EdgeGuard – Motor Fault Detection and Monitoring System

"GitHub Repository" (https://github.com/Sharonhoney05/EdgeGuard)