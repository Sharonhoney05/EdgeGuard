EdgeGuard – Motor Condition Monitoring and Fault Detection System

"EdgeGuard CI" (https://github.com/Sharonhoney05/EdgeGuard/actions/workflows/tests.yml/badge.svg)

Overview

EdgeGuard is an academic engineering and software project that simulates motor operating conditions and analyzes vibration signals to identify potential motor faults.

The project combines signal processing, rule-based fault detection, machine learning, robustness testing, data storage, and visualization in an integrated motor condition monitoring system.

It demonstrates how software and machine learning techniques can be applied to predictive maintenance and industrial condition monitoring.

Key Features

- Simulated motor vibration signal generation.
- Vibration feature extraction using NumPy.
- Rule-based motor fault classification.
- Random Forest machine learning classifier using scikit-learn.
- Model evaluation using accuracy and confusion matrices.
- Robustness testing under different vibration amplitudes and noise levels.
- SQLite database integration for storing monitoring results.
- CSV data export.
- Interactive monitoring dashboard.
- Automated testing using pytest.
- Continuous Integration using GitHub Actions.
- PDF monitoring report generation.

Technologies Used

Technology| Purpose
Python| Core application
NumPy| Numerical operations and vibration calculations
SciPy| Signal processing
Scikit-learn| Random Forest machine learning
Matplotlib| Data visualization
Tkinter| Dashboard interface
SQLite| Data storage
Pandas| Data handling and analysis
ReportLab| PDF report generation
Pytest| Automated testing
GitHub Actions| Continuous Integration

Project Structure

EdgeGuard/
│
├── motor_fault_simulator.py
├── fault_classifier.py
├── edgeguard_ml_classifier.py
├── edgeguard_robustness_test.py
├── edgeguard_database.py
├── edgeguard_export.py
├── edgeguard_dashboard.py
├── edgeguard_integrated_dashboard.py
├── edgeguard_pdf_report.py
├── test_edgeguard.py
├── requirements.txt
├── README.md
├── EdgeGuard_Monitoring_Report.pdf
│
└── screenshots/
    └── analytics.png

Vibration Feature Extraction

EdgeGuard extracts five statistical and frequency-domain features from each simulated vibration signal:

1. Root Mean Square (RMS)
2. Peak Amplitude
3. Standard Deviation
4. Crest Factor
5. Dominant Frequency

These features help characterize vibration patterns and identify potential abnormal motor operating conditions.

Fault Detection Methodology

1. Rule-Based Classification

EdgeGuard uses a threshold-based decision system to classify simulated motor vibration signals into four operating conditions.

- Normal
- Imbalance
- Misalignment
- Bearing Fault

The classifier evaluates extracted vibration features against predefined thresholds.

2. Machine Learning Classification

EdgeGuard also implements a Random Forest classifier using scikit-learn.

The model is trained using a synthetic vibration dataset containing 800 samples across four fault categories.

Dataset split:

- Training samples: 640
- Testing samples: 160
- Features per sample: 5

The model is evaluated using classification accuracy and a confusion matrix.

Robustness Testing

EdgeGuard includes a separate robustness experiment to evaluate classifier performance under different simulated vibration amplitudes and noise levels.

Experimental Conditions

- Amplitude variation between 0.8x and 1.2x.
- Three amplitude levels: 0.8x, 1.0x, and 1.2x.
- Three noise levels: 0.005, 0.020, and 0.040.

Experimental Results

Amplitude| Noise| Rule-Based Accuracy| Random Forest Accuracy
0.8x| 0.005| 95.00%| 100%
0.8x| 0.020| 100%| 100%
0.8x| 0.040| 93.33%| 100%
1.0x| 0.005| 100%| 100%
1.0x| 0.020| 100%| 100%
1.0x| 0.040| 85.00%| 100%
1.2x| 0.005| 100%| 100%
1.2x| 0.020| 100%| 100%
1.2x| 0.040| 84.17%| 100%

Note: These results are obtained from controlled synthetic simulation experiments and do not represent validation on real industrial motor data.

EdgeGuard Analytics

The analytics dashboard provides visual insights into simulated motor operating conditions and fault detection results.

"EdgeGuard Analytics" (screenshots/analytics.png)

Installation and Setup

Clone the repository:

git clone https://github.com/Sharonhoney05/EdgeGuard.git
cd EdgeGuard

Install dependencies:

pip install -r requirements.txt

Running the Project

Launch the integrated dashboard:

python edgeguard_integrated_dashboard.py

Run the machine learning classifier:

python edgeguard_ml_classifier.py

Run robustness experiments:

python edgeguard_robustness_test.py

Run automated tests:

python -m pytest -q test_edgeguard.py

Testing and Continuous Integration

EdgeGuard uses pytest for automated testing and GitHub Actions to automatically execute the test suite whenever changes are pushed to the repository.

This helps maintain code reliability and verify core project functionality.

Future Enhancements

- Integration with real motor vibration sensors.
- ESP32-based real-time vibration monitoring.
- Deployment of machine learning models on edge devices.
- Advanced predictive maintenance analytics.
- Real-time industrial monitoring capabilities.

Project Significance

EdgeGuard is an academic simulation-based prototype developed to explore motor condition monitoring, vibration analysis, machine learning, and software-based fault detection.

It demonstrates the integration of engineering concepts with Python programming, data analytics, and machine learning techniques for predictive maintenance applications.

Author

F K Sharon

Electronics and Communication Engineering

GitHub: "Sharonhoney05" (https://github.com/Sharonhoney05)

---

⭐ If you find this project interesting, consider giving the repository a star!