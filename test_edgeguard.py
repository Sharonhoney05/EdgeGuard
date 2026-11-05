import csv
import edgeguard_export as exporter
import unittest
import tempfile
import os
import numpy as np
import runpy
import matplotlib
matplotlib.use("Agg")
import edgeguard_dashboard as dashboard
import matplotlib.pyplot as plt
import motor_fault_simulator

import classifier_evaluation as evaluation
import edgeguard_database as database
import edgeguard_pdf_report as pdf_report

from motor_fault_simulator import generate_motor_data
from fault_classifier import extract_features, classify_fault
from unittest.mock import patch


class TestEdgeGuard(unittest.TestCase):

    def test_signal_generation(self):
        conditions = [
            "NORMAL",
            "IMBALANCE",
            "MISALIGNMENT",
            "BEARING FAULT"
        ]

        for condition in conditions:
            t, signal, rms, peak, std_dev = generate_motor_data(condition)

            self.assertEqual(len(signal), 1000)
            self.assertEqual(len(t), 1000)
            self.assertTrue(np.all(np.isfinite(signal)))
            self.assertGreater(rms, 0)
            self.assertGreater(peak, 0)
            self.assertGreater(std_dev, 0)

    def test_feature_extraction(self):
        _, signal, _, _, _ = generate_motor_data("NORMAL")

        features = extract_features(signal)
        rms, peak, std_dev, crest, harmonic_ratio = features

        self.assertTrue(all(np.isfinite(value) for value in features))
        self.assertGreater(rms, 0)
        self.assertGreaterEqual(peak, rms)
        self.assertGreater(crest, 0)
        self.assertGreaterEqual(harmonic_ratio, 0)

    def test_fault_classification(self):
        conditions = [
            "NORMAL",
            "IMBALANCE",
            "MISALIGNMENT",
            "BEARING FAULT"
        ]

        for condition in conditions:
            for _ in range(5):
                _, signal, _, _, _ = generate_motor_data(condition)

                rms, peak, std_dev, crest, harmonic_ratio = (
                    extract_features(signal)
                )

                predicted = classify_fault(
                    rms, peak, crest, harmonic_ratio
                )

                self.assertEqual(predicted, condition)

    def test_database_storage(self):
        original_database = database.DATABASE_NAME

        with tempfile.TemporaryDirectory() as temp_dir:
            database.DATABASE_NAME = os.path.join(
                temp_dir, "test_edgeguard.db"
            )

            try:
                database.create_database()

                database.save_reading(
                    "NORMAL",
                    "NORMAL",
                    0.015,
                    0.032,
                    0.015,
                    2.1,
                    0.01
                )

                records = database.get_all_readings()

                self.assertEqual(len(records), 1)
                self.assertEqual(records[0][2], "NORMAL")
                self.assertEqual(records[0][3], "NORMAL")

            finally:
                database.DATABASE_NAME = original_database

    def test_csv_export(self):

        records = [
            (1, "2026-11-05 09:00:00", "NORMAL", "NORMAL",
             0.015, 0.032, 0.015, 2.1, 0.01)
        ]

        original_directory = os.getcwd()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)

                with patch.object(
                    exporter, "get_all_readings", return_value=records
                ):
                    exporter.export_to_csv()

                self.assertTrue(
                    os.path.exists("edgeguard_monitoring_report.csv")
                )

                with open(
                    "edgeguard_monitoring_report.csv",
                    "r",
                    newline=""
                ) as file:
                    rows = list(csv.reader(file))

                self.assertEqual(len(rows), 2)
                self.assertEqual(rows[0][0], "ID")
                self.assertEqual(rows[1][0], "1")
                self.assertEqual(rows[1][2], "NORMAL")
                self.assertEqual(len(rows[0]), 9)
                self.assertEqual(len(rows[1]), 9)
                self.assertEqual(rows[1][3], "NORMAL")
                self.assertEqual(rows[1][4], "0.015")

            finally:
                os.chdir(original_directory)

    def test_csv_export_no_records(self):

        original_directory = os.getcwd()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)

                with patch.object(
                    exporter, "get_all_readings", return_value=[]
                ):
                    exporter.export_to_csv()

                self.assertFalse(
                    os.path.exists("edgeguard_monitoring_report.csv")
                )

            finally:
                os.chdir(original_directory)

    def test_pdf_report_generation(self):

        records = [
            (1, "2026-11-05 09:00:00", "NORMAL", "NORMAL",
             0.015, 0.032, 0.015, 2.1, 0.01),

            (2, "2026-11-05 09:05:00", "IMBALANCE", "IMBALANCE",
             0.025, 0.052, 0.025, 2.2, 0.02)
        ]

        original_directory = os.getcwd()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)

                with patch.object(
                    pdf_report,
                    "get_all_readings",
                    return_value=records.copy()
                ):
                    pdf_report.generate_pdf_report()

                self.assertTrue(
                    os.path.exists("EdgeGuard_Monitoring_Report.pdf")
                )

                self.assertGreater(
                    os.path.getsize("EdgeGuard_Monitoring_Report.pdf"),
                    0
                )

                with open("EdgeGuard_Monitoring_Report.pdf", "rb") as file:
                    self.assertEqual(file.read(5), b"%PDF-")

                self.assertFalse(
                    os.path.exists("edgeguard_report_chart.png")
                )

            finally:
                os.chdir(original_directory)

    def test_pdf_report_no_records(self):

        original_directory = os.getcwd()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)

                with patch.object(
                    pdf_report,
                    "get_all_readings",
                    return_value=[]
                ):
                    pdf_report.generate_pdf_report()

                self.assertFalse(
                    os.path.exists("EdgeGuard_Monitoring_Report.pdf")
                )

                self.assertFalse(
                    os.path.exists("edgeguard_report_chart.png")
                )

            finally:
                os.chdir(original_directory)

    def test_fault_visualization(self):

        t = np.linspace(0, 10, 1000)
        signal = np.sin(2 * np.pi * t)

        sample_data = (
            t, signal, 0.5, 1.0, 0.3
        )

        with patch.object(
            motor_fault_simulator,
            "generate_motor_data",
            return_value=sample_data
        ) as mock_generator:

            with patch.object(plt, "show") as mock_show:

                runpy.run_module(
                    "fault_visualization",
                    run_name="__main__"
                )

                self.assertEqual(mock_generator.call_count, 4)
                mock_show.assert_called_once()

                fig = plt.gcf()

                self.assertEqual(len(fig.axes), 8)

                titles = [
                    axis.get_title()
                    for axis in fig.axes
                ]

                self.assertEqual(len(titles), 8)

                self.assertTrue(
                    any("Vibration Signal" in title for title in titles)
                )

                self.assertTrue(
                    any("Frequency Spectrum" in title for title in titles)
                )

                plt.close(fig)

    def test_database_creation_twice(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "test.db")

            with patch.object(database, "DATABASE_NAME", db_path):
                database.create_database()
                database.create_database()

                connection = database.sqlite3.connect(db_path)
                cursor = connection.cursor()

                cursor.execute("""
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name='motor_readings'
                """)

                result = cursor.fetchone()
                connection.close()

                self.assertIsNotNone(result)

    def test_database_readings_order(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "test.db")

            with patch.object(database, "DATABASE_NAME", db_path):
                database.create_database()

                database.save_reading(
                    "NORMAL", "NORMAL", 0.1, 0.2, 0.05, 1.5, 0.01
                )

                database.save_reading(
                    "IMBALANCE", "IMBALANCE", 0.3, 0.5, 0.1, 2.0, 0.03
                )

                readings = database.get_all_readings()

                self.assertEqual(len(readings), 2)
                self.assertEqual(readings[0][2], "IMBALANCE")
                self.assertEqual(readings[1][2], "NORMAL")

    def test_classifier_evaluation(self):

        sample_data = (
            np.linspace(0, 1, 1000),
            np.sin(np.linspace(0, 10, 1000)),
            0.1, 0.2, 0.05
        )

        with patch.object(
            evaluation,
            "generate_motor_data",
            return_value=sample_data
        ):

            with patch.object(
                evaluation,
                "extract_features",
                return_value=(0.1, 0.2, 0.05, 2.0, 0.01)
            ):

                with patch.object(
                    evaluation,
                    "classify_fault",
                    side_effect=[
                        condition
                        for condition in evaluation.conditions
                        for _ in range(evaluation.samples_per_condition)
                    ]
                ):

                    with patch.object(plt, "show"):

                        matrix, accuracy = evaluation.run_evaluation()

        self.assertEqual(matrix.shape, (4, 4))
        self.assertEqual(np.trace(matrix), 100)
        self.assertEqual(np.sum(matrix), 100)
        self.assertEqual(accuracy, 100.0)

    def test_classifier_evaluation_confusion_matrix(self):

        sample_data = (
            np.linspace(0, 1, 1000),
            np.sin(np.linspace(0, 10, 1000)),
            0.1, 0.2, 0.05
        )

        with patch.object(
            evaluation,
            "generate_motor_data",
            return_value=sample_data
        ):

            with patch.object(
                evaluation,
                "extract_features",
                return_value=(0.1, 0.2, 0.05, 2.0, 0.01)
            ):

                with patch.object(
                    evaluation,
                    "classify_fault",
                    side_effect=["IMBALANCE"] * 100
                ):

                    with patch.object(plt, "show"):

                        matrix, accuracy = evaluation.run_evaluation()

        self.assertEqual(matrix[0, 1], 25)
        self.assertEqual(matrix[1, 1], 25)
        self.assertEqual(matrix[2, 1], 25)
        self.assertEqual(matrix[3, 1], 25)
        self.assertEqual(accuracy, 25.0)

    def test_calculate_vibration_metrics(self):
        rms, peak = dashboard.calculate_vibration_metrics(
            [0.0, 2.0],
            [0.0, 0.0],
            [0.0, 0.0]
        )

        self.assertAlmostEqual(rms, 1.0)
        self.assertAlmostEqual(peak, 1.0)

    def test_classify_vibration_normal(self):
        result = dashboard.classify_vibration(0.04)

        self.assertEqual(result[0], "NORMAL")

    def test_classify_vibration_warning(self):
        result = dashboard.classify_vibration(0.10)

        self.assertEqual(result[0], "WARNING")

    def test_classify_vibration_abnormal(self):
        result = dashboard.classify_vibration(0.25)

        self.assertEqual(result[0], "ABNORMAL")
    def test_classify_vibration_at_normal_boundary(self):
        result = dashboard.classify_vibration(0.05)
        self.assertEqual(result[0], "WARNING")

    def test_classify_vibration_at_warning_boundary(self):
        result = dashboard.classify_vibration(0.20)
        self.assertEqual(result[0], "ABNORMAL")
    def test_dashboard_reading_normal_phase(self):
            with patch.object(dashboard.random, "uniform", return_value=0):
                x, y, z = dashboard.generate_dashboard_reading(0, 0)

            self.assertAlmostEqual(x, 0.0)
            self.assertAlmostEqual(y, 0.02 * 0.7 * np.sin(1))
            self.assertAlmostEqual(z, 1.0 + 0.02 * 0.5 * np.sin(2))

    def test_dashboard_reading_warning_phase(self):
        with patch.object(dashboard.random, "uniform", return_value=0):
            x, y, z = dashboard.generate_dashboard_reading(100, 0)

            self.assertAlmostEqual(x, 0.0)
            self.assertAlmostEqual(y, 0.15 * 0.7 * np.sin(1))
            self.assertAlmostEqual(z, 1.0 + 0.15 * 0.5 * np.sin(2))

    def test_dashboard_reading_abnormal_phase(self):
        with patch.object(dashboard.random, "uniform", return_value=0):
                x, y, z = dashboard.generate_dashboard_reading(200, 0)

        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, 0.40 * 0.7 * np.sin(1))
        self.assertAlmostEqual(z, 1.0 + 0.40 * 0.5 * np.sin(2))

    def test_monitoring_state_initially_running(self):
        state = dashboard.MonitoringState()
        self.assertTrue(state.running)

    def test_monitoring_state_stop(self):
        state = dashboard.MonitoringState()
        state.stop()
        self.assertFalse(state.running)

    def test_monitoring_state_start(self):
        state = dashboard.MonitoringState()
        state.stop()

        result = state.start()

        self.assertTrue(result)
        self.assertTrue(state.running)

    def test_database_stores_all_reading_values(self):

        with tempfile.TemporaryDirectory() as temp_dir:
            original_database = database.DATABASE_NAME
            database.DATABASE_NAME = os.path.join(
                temp_dir, "test.db"
            )

            try:
                database.create_database()

                database.save_reading(
                    "NORMAL",
                    "NORMAL",
                    0.05,
                    0.10,
                    0.03,
                    2.0,
                    0.01
                )

                records = database.get_all_readings()

                self.assertEqual(len(records), 1)
                self.assertEqual(records[0][2], "NORMAL")
                self.assertEqual(records[0][3], "NORMAL")
                self.assertAlmostEqual(records[0][4], 0.05)
                self.assertAlmostEqual(records[0][5], 0.10)
                self.assertAlmostEqual(records[0][6], 0.03)
                self.assertAlmostEqual(records[0][7], 2.0)
                self.assertAlmostEqual(records[0][8], 0.01)

            finally:
                database.DATABASE_NAME = original_database

    def test_database_returns_empty_list(self):

        with tempfile.TemporaryDirectory() as temp_dir:
            original_database = database.DATABASE_NAME
            database.DATABASE_NAME = os.path.join(
                temp_dir, "empty.db"
            )

            try:
                database.create_database()

                records = database.get_all_readings()

                self.assertEqual(records, [])

            finally:
                database.DATABASE_NAME = original_database

if __name__ == "__main__":
    unittest.main(verbosity=2)
