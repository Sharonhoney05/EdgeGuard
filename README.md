EdgeGuard - Motor Condition Monitoring and Fault Detection System

A Python-based simulation prototype for vibration analysis, motor fault classification, and predictive maintenance monitoring.

Overview

EdgeGuard is an academic engineering project that simulates motor operating conditions and analyzes vibration data to identify potential motor faults.

It combines signal analysis, feature extraction, fault classification, SQLite database management, interactive visualization, and automated PDF reporting in one application.

Important: This project currently uses simulated vibration data. It is not connected to physical motor sensors and is not intended for validated industrial diagnosis.

Key Features

- Motor Fault Simulation: Generates vibration data for normal, imbalance, misalignment, and bearing fault conditions.
- Vibration Analysis: Calculates statistical features such as RMS, peak, standard deviation, crest factor, and harmonic ratio.
- Fault Classification: Classifies simulated motor conditions using the project's classification logic.
- Interactive Dashboard: Displays live simulated readings and motor condition status using Tkinter.
- Monitoring History: Stores and displays historical readings using SQLite.
- Data Visualization: Presents vibration trends and classification analytics using Matplotlib.
- CSV Export: Exports stored monitoring records.
- PDF Reporting: Generates a report containing monitoring statistics, fault distribution, historical analysis, and detailed records.
- Automated Testing: Includes a pytest test suite.

Technologies Used

Technology| Purpose
Python| Core application
NumPy| Numerical and vibration calculations
Tkinter| Graphical user interface
Matplotlib| Data visualization
SQLite| Monitoring data storage
ReportLab| PDF report generation
CSV| Data export
Pytest| Automated testing

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
|-- fault_visualization.py
|-- edgeguard_database.py
|-- edgeguard_export.py
|-- edgeguard_dashboard.py
|-- edgeguard_integrated_dashboard.py
|-- edgeguard_pdf_report.py
|-- test_edgeguard.py
|-- README.md
|-- .gitignore

System Architecture

1. The motor fault simulator generates vibration samples for different operating conditions.
2. The feature extraction module calculates vibration characteristics.
3. The fault classifier predicts the motor condition.
4. The SQLite database stores monitoring readings and calculated features.
5. The integrated dashboard displays readings, graphs, and motor condition information.
6. Users can view historical records and export monitoring data.
7. The PDF generator produces a monitoring report from stored records.

Installation and Setup

1. Clone the repository

git clone https://github.com/Sharonhoney05/EdgeGuard.git

2. Navigate to the project directory

cd EdgeGuard

3. Install dependencies

pip install numpy matplotlib reportlab pytest

Tkinter and SQLite are included with most standard Python installations.

4. Launch the integrated dashboard

python edgeguard_integrated_dashboard.py

5. Run automated tests

python -m pytest

Screenshots

Motor Fault Classification

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

"Detailed Monitoring History" (screenshots/view_history_details.png)

Analytics Dashboard

"EdgeGuard Analytics" (screenshots/analytics.png)

Applications

- Motor condition monitoring concepts
- Vibration-based fault detection
- Predictive maintenance
- Industrial automation
- Industrial IoT applications
- Equipment health monitoring

Future Enhancements

- Integration with physical vibration sensors.
- ESP32-based wireless motor monitoring.
- Machine learning-based fault classification.
- Cloud-based monitoring and analytics.
- Real-time abnormal-condition alerts.

Testing

The project includes automated tests covering simulation, vibration calculations, fault classification, database operations, and report generation.

Latest verified test result: 27 tests passed.

Author

F K Sharon
Electronics and Communication Engineering

Project Disclaimer

EdgeGuard is an academic simulation-based prototype developed to explore motor condition monitoring, vibration analysis, and software-based fault detection. Its simulated results should not be interpreted as real industrial measurements.