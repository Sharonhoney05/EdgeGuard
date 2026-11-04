import sqlite3
from datetime import datetime

DATABASE_NAME = "edgeguard.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS motor_readings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            selected_condition TEXT,

            predicted_condition TEXT,

            rms REAL,

            peak REAL,

            standard_deviation REAL,

            crest_factor REAL,

            harmonic_ratio REAL

        )
    """)

    connection.commit()
    connection.close()

    print("EdgeGuard database created successfully!")


def save_reading(
    selected_condition,
    predicted_condition,
    rms,
    peak,
    std_dev,
    crest,
    harmonic_ratio
):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO motor_readings (

            timestamp,
            selected_condition,
            predicted_condition,
            rms,
            peak,
            standard_deviation,
            crest_factor,
            harmonic_ratio

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (
        timestamp,
        selected_condition,
        predicted_condition,
        rms,
        peak,
        std_dev,
        crest,
        harmonic_ratio
    ))

    connection.commit()
    connection.close()


def get_all_readings():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM motor_readings
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records


if __name__ == "__main__":

    create_database()

    print("\nTesting database storage...")

    save_reading(
        "IMBALANCE",
        "IMBALANCE",
        0.106,
        0.163,
        0.106,
        1.53,
        0.003
    )

    readings = get_all_readings()

    print("\nStored Monitoring Records:")

    for reading in readings:
        print(reading)