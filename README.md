EdgeGuard – Motor Condition Monitoring and Fault Detection System

A Python-based simulation prototype for vibration analysis, motor fault classification, machine learning-based detection, and predictive maintenance monitoring.

Overview

EdgeGuard is an academic engineering project that simulates motor operating conditions and analyzes vibration signals to identify potential motor faults.

It combines signal processing, statistical feature extraction, rule-based classification, Random Forest machine learning, robustness evaluation, SQLite database management, interactive visualization, automated testing, and PDF reporting.

Project status: Simulation-based prototype. The current implementation uses generated vibration signals and is not connected to physical motor sensors.

Key Features

- Motor Fault Simulation: Generates vibration signals for normal, imbalance, misalignment, and bearing fault conditions.
- Vibration Feature Extraction: Calculates RMS, peak amplitude, standard deviation, crest factor, and harmonic ratio.
- Rule-Based Fault Classification: Uses signal features and threshold-based decision rules.
- Machine Learning Classification: Implements a Random Forest classifier using scikit-learn.
- Classifier Evaluation: Evaluates classification performance using accuracy, precision, recall, F1-score, and confusion matrices.
- Robustness Testing: Evaluates both classifiers under different amplitude and noise conditions.
- Interactive Dashboard: Displays simulated readings and motor condition status using Tkinter.
- Monitoring History: Stores and retrieves monitoring records using SQLite.
- Data Visualization: Displays vibration trends and classification analytics using Matplotlib.
- CSV Export: Exports monitoring records and evaluation results.
- PDF Reporting: Generates reports containing monitoring statistics, fault distribution, historical analysis, and detailed records.
- Automated Testing: Includes tests for major project components.

Technologies Used

Technology| Purpose
Python| Core application
NumPy| Numerical and vibration calculations
scikit-learn| Random Forest machine learning
Tkinter| Graphical user interface
Matplotlib| Data visualization and evaluation plots
SQLite| Monitoring data storage
ReportLab| PDF report generation
CSV| Data export and evaluation results
unittest| Automated testing

Project Structure

EdgeGuard/
|
|-- Day1/
|   |-- vibration_basics.py
|
|-- screenshots/
|   |-- normal.png
|   |-- bearing_fault.png
|   |-- imbalance.png
|   |-- misalignment.png
|   |-- view_history.png
|   |-- view_history_details.png
|   |-- analytics.png
|
|-- motor_fault_simulator.py
|-- fault_classifier.py
|-- classifier_evaluation.py
|-- edgeguard_ml_classifier.py
|-- edgeguard_robustness_test.py
|-- fault_visualization.py
|-- edgeguard_database.py
|-- edgeguard_export.py
|-- edgeguard_dashboard.py
|-- edgeguard_integrated_dashboard.py
|-- edgeguard_pdf_report.py
|-- test_edgeguard.py
|-- evaluation_results.csv
|-- confusion_matrix.png
|-- ml_confusion_matrix.png
|-- model_comparison.csv
|-- robustness_results.csv
|-- robustness_comparison.png
|-- README.md
|-- .gitignore

System Architecture

1. Signal Generation: The motor fault simulator generates vibration signals for four operating conditions.
2. Feature Extraction: Statistical and frequency-domain features are extracted from each vibration signal.
3. Fault Classification: A rule-based classifier analyzes extracted features and predicts motor conditions.
4. Machine Learning: A Random Forest model learns patterns from extracted vibration features.
5. Evaluation: Both classifiers are evaluated using synthetic test datasets.
6. Robustness Analysis: Classifier performance is compared under different amplitude and noise conditions.
7. Database Management: SQLite stores monitoring readings and calculated features.
8. Dashboard: The integrated dashboard displays readings, graphs, and motor condition information.
9. Reporting: Users can view historical records, export CSV data, and generate PDF reports.

Fault Classification Methodology

Feature Extraction

EdgeGuard extracts five features from each vibration signal:

- RMS: Measures the overall vibration level.
- Peak amplitude: Measures the maximum absolute vibration amplitude.
- Standard deviation: Measures signal variation around its mean.
- Crest factor: Ratio of peak amplitude to RMS.
- Harmonic ratio: Compares the 10 Hz harmonic magnitude with the 5 Hz fundamental magnitude.

Rule-Based Classification

The current decision rules are:

Condition| Classification Rule
Bearing Fault| Peak amplitude > 0.25 and crest factor > 2.5
Misalignment| Harmonic ratio > 0.4
Imbalance| RMS > 0.05
Normal| None of the above conditions are met

These thresholds were selected for the current simulated signal patterns. They are experimental project parameters, not universal industrial diagnostic limits.

Random Forest Classification

EdgeGuard also implements a Random Forest classifier using scikit-learn.

Model configuration:

- Algorithm: Random Forest
- Number of estimators: 200
- Input features: Five extracted vibration features
- Training dataset: 800 synthetic samples
- Testing dataset: 160 synthetic samples
- Train-test split: 80:20
- Random state: 42
- Class weighting: Balanced

The model is evaluated against the existing rule-based classifier using the same held-out test samples.

Classifier Evaluation

The original rule-based evaluation module tests 100 synthetic vibration samples:

- 25 Normal samples
- 25 Imbalance samples
- 25 Misalignment samples
- 25 Bearing Fault samples

Evaluation metrics include:

- Accuracy
- Per-class precision
- Per-class recall
- Per-class F1-score
- Confusion matrix
- CSV evaluation results

Original Synthetic Evaluation Results

Metric| Result
Test samples| 100
Correct predictions| 100
Incorrect predictions| 0
Accuracy| 100%
Macro precision| 100%
Macro recall| 100%
Macro F1-score| 100%

Random Forest Evaluation

The Random Forest classifier is evaluated on 160 held-out synthetic samples.

Both the rule-based and Random Forest classifiers achieved 100% accuracy on this particular test split.

Generated outputs:

- "ml_confusion_matrix.png"
- "model_comparison.csv"

Robustness Testing

EdgeGuard includes a separate robustness experiment to evaluate classifier performance under different simulated vibration amplitudes and noise levels.

Experimental Configuration

Training dataset:

- 1,200 synthetic vibration signals.
- 300 samples per fault category.
- Random amplitude variation between 0.8× and 1.2×.
- Random noise standard deviation between 0.005 g and 0.04 g.

Testing dataset:

- Four fault categories.
- Three amplitude levels: 0.8×, 1.0×, and 1.2×.
- Three noise levels: 0.005 g, 0.02 g, and 0.04 g.
- 30 test repetitions per fault category for each scenario.
- 120 test signals per scenario.
- 1,080 total test signals.

Robustness Results

Amplitude| Noise (g)| Rule-Based Accuracy| Random Forest Accuracy
0.8×| 0.005| 95.00%| 100%
0.8×| 0.020| 100%| 100%
0.8×| 0.040| 93.33%| 100%
1.0×| 0.005| 100%| 100%
1.0×| 0.020| 100%| 100%
1.0×| 0.040| 85.00%| 100%
1.2×| 0.005| 100%| 100%
1.2×| 0.020| 100%| 100%
1.2×| 0.040| 84.17%| 100%

Overall Performance Comparison

Metric| Rule-Based| Random Forest
Average scenario accuracy| 95.28%| 100%

The Random Forest classifier achieved 100% accuracy across the nine tested simulation scenarios. The rule-based classifier showed reduced accuracy under certain higher-noise conditions.

Generated outputs:

- "robustness_results.csv"
- "robustness_comparison.png"

Robustness evaluation limitation: Training and testing signals use the same underlying simulated fault patterns. The experiment evaluates sensitivity to the selected amplitude and noise variations, not generalization to previously unseen physical motor faults.

Installation and Setup

1. Clone the repository

git clone https://github.com/Sharonhoney05/EdgeGuard.git

2. Navigate to the project directory

cd EdgeGuard

3. Install dependencies

pip install numpy matplotlib reportlab scikit-learn

Tkinter and SQLite are included with most standard Python installations.

4. Launch the integrated dashboard

python edgeguard_integrated_dashboard.py

5. Run classifier evaluation

python classifier_evaluation.py

Generates "evaluation_results.csv" and "confusion_matrix.png".

6. Run Random Forest evaluation

python edgeguard_ml_classifier.py

Generates "ml_confusion_matrix.png" and "model_comparison.csv".

7. Run robustness testing

python edgeguard_robustness_test.py

Generates "robustness_results.csv" and "robustness_comparison.png".

8. Run automated tests

python -m unittest test_edgeguard.py -v

Dashboard Screenshots

Normal Condition

"Normal Condition" (screenshots/normal.png)

Bearing Fault

"Bearing Fault" (screenshots/bearing_fault.png)

Imbalance

"Imbalance" (screenshots/imbalance.png)

Misalignment

"Misalignment" (screenshots/misalignment.png)

Monitoring History

"Monitoring History" (screenshots/view_history.png)

Detailed Monitoring History

"Detailed Monitoring History" (screenshots/view_history_details.png)

EdgeGuard Analytics

"EdgeGuard Analytics" (screenshots/analytics.png)

Applications

- Motor condition monitoring concepts
- Vibration-based fault detection
- Predictive maintenance
- Industrial automation
- Industrial IoT applications
- Equipment health monitoring

Future Enhancements

- Evaluation using publicly available real vibration datasets.
- Validation using physical vibration sensors.
- ESP32-based wireless motor monitoring.
- Real-time abnormal-condition alerts.
- Cloud-based monitoring and analytics.
- Improved fault classification using more diverse signal patterns.
- Evaluation using real-world motor operating conditions.

Testing

The project includes automated tests covering simulation, vibration calculations, fault classification, classifier evaluation, database operations, data export, dashboard functionality, and report generation.

Previously verified automated test result: 27 tests passed.

Author

F K Sharon
Electronics and Communication Engineering

Project Disclaimer

EdgeGuard is an academic simulation-based prototype developed to explore motor condition monitoring, vibration analysis, machine learning, and software-based fault detection.

All reported evaluation and robustness results are based on synthetic vibration signals. They should not be interpreted as real industrial measurements or validated diagnostic performance.