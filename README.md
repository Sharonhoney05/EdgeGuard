EdgeGuard – Motor Condition Monitoring and Fault Detection System

A Python-based simulation prototype for vibration analysis, motor fault classification, machine learning evaluation, and predictive maintenance monitoring.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-orange)
![EdgeGuard CI](https://github.com/Sharonhoney05/EdgeGuard/actions/workflows/tests.yml/badge.svg)
![Project](https://img.shields.io/badge/Project-Simulation%20Based-purple)

Overview

EdgeGuard is an academic engineering project that simulates motor operating conditions and analyzes vibration signals to identify potential motor faults.

It combines signal processing, statistical feature extraction, rule-based classification, Random Forest machine learning, robustness evaluation, SQLite database management, interactive visualization, automated testing, and PDF reporting.

Project status: Simulation-based prototype. The current implementation uses generated vibration signals and is not connected to physical motor sensors.

Key Features

- Motor Fault Simulation: Generates vibration signals for normal, imbalance, misalignment, and bearing fault conditions.
- Feature Extraction: Calculates RMS, peak amplitude, standard deviation, crest factor, and harmonic ratio.
- Rule-Based Classification: Identifies motor conditions using experimental decision thresholds.
- Machine Learning: Implements a Random Forest classifier using scikit-learn.
- Performance Evaluation: Measures accuracy, precision, recall, F1-score, and confusion matrices.
- Robustness Testing: Compares classifiers under different simulated amplitude and noise conditions.
- Interactive Dashboard: Displays simulated readings and motor condition status using Tkinter.
- Monitoring History: Stores and retrieves monitoring records using SQLite.
- Data Visualization: Displays vibration trends and classification analytics using Matplotlib.
- CSV Export: Exports monitoring records and evaluation results.
- PDF Reporting: Generates reports containing monitoring statistics, fault distribution, historical analysis, and detailed records.
- Automated Testing: Includes a unittest suite covering major project components.

Technologies Used

Technology| Purpose
Python| Core application
NumPy| Numerical operations and vibration calculations
scikit-learn| Random Forest machine learning
Tkinter| Graphical user interface
Matplotlib| Data visualization and evaluation plots
SQLite| Monitoring data storage
ReportLab| PDF report generation
CSV| Data export and evaluation results
unittest| Automated testing

System Architecture

        Motor Fault Simulator
                  |
                  v
          Vibration Signals
                  |
                  v
           Feature Extraction
                  |
          +-------+-------+
          |               |
          v               v
    Rule-Based        Random Forest
    Classifier          Model
          |               |
          +-------+-------+
                  |
                  v
          Performance Evaluation
                  |
                  v
           Robustness Testing
                  |
                  v
          Integrated Dashboard
                  |
          +-------+-------+
          |               |
          v               v
       SQLite         Visualization
       Database        and Reports

Project Structure

EdgeGuard/
│
├── Day1/
│   └── vibration_basics.py
│
├── screenshots/
│   ├── normal.png
│   ├── bearing_fault.png
│   ├── imbalance.png
│   ├── misalignment.png
│   ├── view_history.png
│   ├── view_history_details.png
│   └── analytics.png
│
├── motor_fault_simulator.py
├── fault_classifier.py
├── classifier_evaluation.py
├── edgeguard_ml_classifier.py
├── edgeguard_robustness_test.py
├── fault_visualization.py
├── edgeguard_database.py
├── edgeguard_export.py
├── edgeguard_dashboard.py
├── edgeguard_integrated_dashboard.py
├── edgeguard_pdf_report.py
├── test_edgeguard.py
│
├── evaluation_results.csv
├── confusion_matrix.png
├── ml_confusion_matrix.png
├── model_comparison.csv
├── robustness_results.csv
├── robustness_comparison.png
│
├── EdgeGuard_Monitoring_Report.pdf
├── README.md
└── .gitignore

Fault Classification Methodology

1. Vibration Feature Extraction

EdgeGuard extracts five features from each simulated vibration signal:

Feature| Description
RMS| Measures overall vibration level
Peak Amplitude| Measures maximum absolute vibration amplitude
Standard Deviation| Measures signal variation around its mean
Crest Factor| Ratio of peak amplitude to RMS
Harmonic Ratio| Compares the 10 Hz harmonic magnitude with the 5 Hz fundamental magnitude

2. Rule-Based Classification

The current experimental decision rules are:

Condition| Classification Rule
Bearing Fault| Peak amplitude > 0.25 and crest factor > 2.5
Misalignment| Harmonic ratio > 0.4
Imbalance| RMS > 0.05
Normal| None of the above conditions are met

These thresholds were selected for the current simulated signal patterns. They are experimental project parameters, not universal industrial diagnostic limits.

3. Random Forest Classification

EdgeGuard also implements a Random Forest classifier using scikit-learn.

Model configuration

Parameter| Value
Algorithm| Random Forest
Number of estimators| 200
Input features| 5
Training dataset| 800 synthetic samples
Testing dataset| 160 synthetic samples
Train-test split| 80:20
Random state| 42
Class weighting| Balanced

The model is evaluated against the existing rule-based classifier using the same held-out test samples.

Classifier Evaluation

Rule-Based Evaluation

The standalone rule-based evaluation module tests 100 synthetic vibration samples:

- 25 Normal samples
- 25 Imbalance samples
- 25 Misalignment samples
- 25 Bearing Fault samples

Evaluation results

Metric| Result
Total test samples| 100
Correct predictions| 100
Incorrect predictions| 0
Accuracy| 100%
Macro Precision| 100%
Macro Recall| 100%
Macro F1-score| 100%

The generated confusion matrix contains 25 correct predictions for each of the four classes.

Random Forest Evaluation

The Random Forest model is evaluated using 160 held-out synthetic samples, with 40 samples per class.

Model comparison

Metric| Rule-Based| Random Forest
Accuracy| 100%| 100%
Macro Precision| 100%| 100%
Macro Recall| 100%| 100%
Macro F1-score| 100%| 100%

Generated outputs:

- "ml_confusion_matrix.png"
- "model_comparison.csv"

Robustness Testing

EdgeGuard includes a separate robustness experiment to evaluate classifier performance under different simulated vibration amplitudes and noise levels.

Experimental Configuration

Training dataset

- 1,200 synthetic vibration signals.
- 300 samples per fault category.
- Amplitude variation between 0.8× and 1.2×.
- Noise standard deviation between 0.005 g and 0.04 g.

Testing dataset

- Four fault categories.
- Three amplitude levels: 0.8×, 1.0×, and 1.2×.
- Three noise levels: 0.005 g, 0.02 g, and 0.04 g.
- 30 repetitions per fault category for each scenario.
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

Average scenario accuracy

Classifier| Average Accuracy
Rule-Based| 95.28%
Random Forest| 100%

The Random Forest classifier achieved 100% accuracy across the nine tested simulation scenarios. The rule-based classifier showed reduced accuracy under certain higher-noise conditions.

Generated outputs:

- "robustness_results.csv"
- "robustness_comparison.png"

Robustness limitation: Training and testing signals use the same underlying simulated fault patterns. This experiment evaluates sensitivity to the selected amplitude and noise variations, not generalization to previously unseen physical motor faults.

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

Installation and Setup

1. Clone the repository

git clone https://github.com/Sharonhoney05/EdgeGuard.git

2. Navigate to the project directory

cd EdgeGuard

3. Install dependencies

pip install numpy matplotlib reportlab scikit-learn

Tkinter and SQLite are included with most standard Python installations. Tkinter availability depends on the Python installation.

4. Launch the integrated dashboard

python edgeguard_integrated_dashboard.py

5. Run rule-based classifier evaluation

python classifier_evaluation.py

Generates:

- "evaluation_results.csv"
- "confusion_matrix.png"

6. Run Random Forest evaluation

python edgeguard_ml_classifier.py

Generates:

- "ml_confusion_matrix.png"
- "model_comparison.csv"

7. Run robustness testing

python edgeguard_robustness_test.py

Generates:

- "robustness_results.csv"
- "robustness_comparison.png"

8. Run automated tests

python -m unittest test_edgeguard.py -v

Testing

The project includes automated tests covering:

- Vibration signal simulation
- Feature extraction
- Fault classification
- Classifier evaluation
- Database operations
- CSV export
- Dashboard functionality
- PDF report generation

Previously verified result: 27 tests passed.

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

Author

F K Sharon
Electronics and Communication Engineering

Project Disclaimer

EdgeGuard is an academic simulation-based prototype developed to explore motor condition monitoring, vibration analysis, machine learning, and software-based fault detection.

All reported evaluation and robustness results are based on synthetic vibration signals. They should not be interpreted as real industrial measurements or validated diagnostic performance.

The project is intended for educational and experimental purposes.