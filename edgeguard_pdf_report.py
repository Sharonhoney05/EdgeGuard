import os
import matplotlib.pyplot as plt

from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)

from edgeguard_database import get_all_readings


def generate_pdf_report():

    records = get_all_readings()

    if not records:
        print("No monitoring records available!")
        return

    records.reverse()

    filename = "EdgeGuard_Monitoring_Report.pdf"

    # Extract database values
    rms_values = [row[4] for row in records]
    predictions = [row[3] for row in records]

    total_records = len(records)
    average_rms = sum(rms_values) / total_records
    minimum_rms = min(rms_values)
    maximum_rms = max(rms_values)

    conditions = [
        "NORMAL",
        "IMBALANCE",
        "MISALIGNMENT",
        "BEARING FAULT"
    ]

    fault_counts = [
        predictions.count(condition)
        for condition in conditions
    ]

    # Generate historical chart
    chart_filename = "edgeguard_report_chart.png"

    plt.figure(figsize=(9, 4))

    plt.plot(
        range(1, total_records + 1),
        rms_values,
        marker="o"
    )

    plt.title("Historical Vibration RMS Trend")
    plt.xlabel("Reading Number")
    plt.ylabel("RMS (g)")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(chart_filename, dpi=150)
    plt.close()

    # Create PDF
    pdf = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )

    styles = getSampleStyleSheet()
    content = []

    # Title
    content.append(
        Paragraph(
            "<b>EDGEGUARD</b>",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            "Motor Condition Monitoring System",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            "SIMULATION-BASED PROJECT REPORT",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            "Report Generated: "
            + datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 15))

    # Monitoring summary
    content.append(
        Paragraph(
            "1. MONITORING SUMMARY",
            styles["Heading2"]
        )
    )

    summary_data = [
        ["Metric", "Value"],
        ["Total Records", str(total_records)],
        ["Average RMS", f"{average_rms:.4f} g"],
        ["Minimum RMS", f"{minimum_rms:.4f} g"],
        ["Maximum RMS", f"{maximum_rms:.4f} g"]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[75 * mm, 75 * mm]
    )

    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("ALIGN", (0, 0), (-1, -1), "CENTER")
        ])
    )

    content.append(summary_table)
    content.append(Spacer(1, 20))

    # Fault distribution
    content.append(
        Paragraph(
            "2. FAULT DISTRIBUTION",
            styles["Heading2"]
        )
    )

    fault_data = [["Motor Condition", "Number of Readings"]]

    for condition, count in zip(conditions, fault_counts):
        fault_data.append([condition, str(count)])

    fault_table = Table(
        fault_data,
        colWidths=[75 * mm, 75 * mm]
    )

    fault_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("ALIGN", (0, 0), (-1, -1), "CENTER")
        ])
    )

    content.append(fault_table)
    content.append(Spacer(1, 20))

    # Historical chart
    content.append(
        Paragraph(
            "3. HISTORICAL VIBRATION ANALYSIS",
            styles["Heading2"]
        )
    )

    content.append(
        Image(
            chart_filename,
            width=165 * mm,
            height=75 * mm
        )
    )

    content.append(Spacer(1, 15))

    # Detailed records
    content.append(
        Paragraph(
            "4. MONITORING RECORDS",
            styles["Heading2"]
        )
    )

    detail_data = [
        ["ID", "Timestamp", "Selected", "Predicted", "RMS (g)"]
    ]

    for row in records:
        detail_data.append([
            str(row[0]),
            str(row[1]),
            str(row[2]),
            str(row[3]),
            f"{row[4]:.4f}"
        ])

    detail_table = Table(
        detail_data,
        repeatRows=1,
        colWidths=[
            12 * mm,
            43 * mm,
            35 * mm,
            35 * mm,
            20 * mm
        ]
    )

    detail_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("PADDING", (0, 0), (-1, -1), 5),
            ("ALIGN", (0, 0), (-1, -1), "CENTER")
        ])
    )

    content.append(detail_table)

    content.append(Spacer(1, 20))

    # Disclaimer
    content.append(
        Paragraph(
            "<b>Note:</b> All readings in this report are "
            "simulated data generated by the EdgeGuard prototype. "
            "They are not real sensor measurements or validated "
            "industrial diagnostic results.",
            styles["Italic"]
        )
    )

    pdf.build(content)

    # Remove temporary chart
    if os.path.exists(chart_filename):
        os.remove(chart_filename)

    print("\n===================================")
    print(" EDGEGUARD PDF REPORT GENERATED")
    print("===================================")
    print("Total records:", total_records)
    print("Average RMS:", round(average_rms, 4), "g")
    print("PDF file:", filename)


if __name__ == "__main__":
    generate_pdf_report()