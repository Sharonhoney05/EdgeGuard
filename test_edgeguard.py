import unittest
import tempfile
import os
import numpy as np

import edgeguard_database as database

from motor_fault_simulator import generate_motor_data
from fault_classifier import extract_features, classify_fault


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


if __name__ == "__main__":
    unittest.main(verbosity=2)