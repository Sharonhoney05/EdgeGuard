import csv
from edgeguard_database import get_all_readings


def export_to_csv():

    records = get_all_readings()

    if not records:
        print("No monitoring records available!")
        return

    filename = "edgeguard_monitoring_report.csv"

    headers = [
        "ID",
        "Timestamp",
        "Selected Condition",
        "Predicted Condition",
        "RMS",
        "Peak",
        "Standard Deviation",
        "Crest Factor",
        "Harmonic Ratio"
    ]

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(headers)

        writer.writerows(records)

    print("\n================================")
    print(" EDGEGUARD CSV EXPORT")
    print("================================")

    print("Total records exported:", len(records))
    print("File created:", filename)


if __name__ == "__main__":

    export_to_csv()