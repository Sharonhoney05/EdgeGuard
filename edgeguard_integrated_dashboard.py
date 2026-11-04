import csv
import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from motor_fault_simulator import generate_motor_data
from fault_classifier import extract_features, classify_fault
from edgeguard_database import (
    create_database,
    save_reading,
    get_all_readings
)


class EdgeGuardDashboard:

    def __init__(self, root):

        self.root = root
        self.root.title("EDGEGUARD - Motor Condition Monitoring")
        self.root.geometry("1100x800")

        self.monitoring = False
        self.after_id = None

        create_database()

        self.root.configure(bg="#17212b")

        tk.Label(
            root,
            text="EDGEGUARD - MOTOR MONITORING SYSTEM",
            font=("Arial", 20, "bold"),
            bg="#17212b",
            fg="white"
        ).pack(pady=15)

        tk.Label(
            root,
            text="SIMULATION PROTOTYPE - NOT REAL SENSOR DATA",
            font=("Arial", 10, "bold"),
            bg="#17212b",
            fg="#f0c674"
        ).pack()

        control_frame = tk.Frame(root, bg="#17212b")
        control_frame.pack(pady=15)

        tk.Label(
            control_frame,
            text="Select Motor Condition:",
            font=("Arial", 12),
            bg="#17212b",
            fg="white"
        ).pack(side=tk.LEFT, padx=8)

        self.condition = tk.StringVar(value="NORMAL")

        self.dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.condition,
            values=[
                "NORMAL",
                "IMBALANCE",
                "MISALIGNMENT",
                "BEARING FAULT"
            ],
            state="readonly",
            width=20
        )
        self.dropdown.pack(side=tk.LEFT, padx=8)

        self.start_button = tk.Button(
            control_frame,
            text="START MONITORING",
            command=self.start_monitoring,
            bg="#238636",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(
            control_frame,
            text="STOP",
            command=self.stop_monitoring,
            bg="#da3633",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.history_button = tk.Button(
            control_frame,
            text="VIEW HISTORY",
            command=self.show_history,
            bg="#1f6feb",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.history_button.pack(side=tk.LEFT, padx=5)

        self.export_button = tk.Button(
            control_frame,
            text="EXPORT TO CSV",
            command=self.export_history,
            bg="#8957e5",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.export_button.pack(side=tk.LEFT, padx=5)

        self.analytics_button = tk.Button(
            control_frame,
            text="VIEW ANALYTICS",
            command=self.show_analytics,
            bg="#168aad",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.analytics_button.pack(side=tk.LEFT, padx=5)

        # Metrics section

        metrics = tk.Frame(root, bg="#17212b")
        metrics.pack(pady=10)

        self.rms_label = self.create_metric(
            metrics, "Vibration RMS"
        )

        self.peak_label = self.create_metric(
            metrics, "Peak"
        )

        self.crest_label = self.create_metric(
            metrics, "Crest Factor"
        )

        self.status_label = tk.Label(
            root,
            text="SYSTEM READY",
            font=("Arial", 16, "bold"),
            bg="#17212b",
            fg="#58a6ff"
        )
        self.status_label.pack(pady=10)

        self.prediction_label = tk.Label(
            root,
            text="Predicted Condition: --",
            font=("Arial", 14, "bold"),
            bg="#17212b",
            fg="white"
        )
        self.prediction_label.pack(pady=5)

        # Main dashboard graphs

        self.fig, self.axes = plt.subplots(
            2, 1, figsize=(9, 5)
        )

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=root
        )

        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True,
            padx=15,
            pady=10
        )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_dashboard
        )

    def create_metric(self, parent, name):

        frame = tk.Frame(
            parent,
            bg="#263442",
            padx=20,
            pady=10
        )
        frame.pack(side=tk.LEFT, padx=10)

        tk.Label(
            frame,
            text=name,
            bg="#263442",
            fg="white",
            font=("Arial", 11)
        ).pack()

        value = tk.Label(
            frame,
            text="--",
            bg="#263442",
            fg="#58a6ff",
            font=("Arial", 18, "bold")
        )
        value.pack()

        return value

    def start_monitoring(self):

        if self.monitoring:
            return

        self.monitoring = True

        self.start_button.config(state=tk.DISABLED)
        self.dropdown.config(state="disabled")

        self.status_label.config(
            text="MONITORING ACTIVE",
            fg="#3fb950"
        )

        self.update_dashboard()

    def stop_monitoring(self):

        self.monitoring = False

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.start_button.config(state=tk.NORMAL)
        self.dropdown.config(state="readonly")

        self.status_label.config(
            text="MONITORING STOPPED",
            fg="#f0c674"
        )

    def update_dashboard(self):

        if not self.monitoring:
            return

        condition = self.condition.get()

        t, signal, _, _, _ = generate_motor_data(condition)

        rms, peak, std_dev, crest, harmonic_ratio = (
            extract_features(signal)
        )

        prediction = classify_fault(
            rms,
            peak,
            crest,
            harmonic_ratio
        )

        # Update dashboard metrics

        self.rms_label.config(
            text=f"{rms:.4f} g"
        )

        self.peak_label.config(
            text=f"{peak:.4f} g"
        )

        self.crest_label.config(
            text=f"{crest:.2f}"
        )

        self.prediction_label.config(
            text=f"Predicted Condition: {prediction}"
        )

        if prediction == "NORMAL":

            self.status_label.config(
                text="STATUS: NORMAL",
                fg="#3fb950"
            )

        elif prediction == "BEARING FAULT":

            self.status_label.config(
                text="ALERT: BEARING FAULT",
                fg="#ff7b72"
            )

        else:

            self.status_label.config(
                text=f"WARNING: {prediction}",
                fg="#f0c674"
            )

        # Save reading to SQLite

        save_reading(
            condition,
            prediction,
            rms,
            peak,
            std_dev,
            crest,
            harmonic_ratio
        )

        # Update vibration waveform

        self.axes[0].clear()
        self.axes[0].plot(t, signal)

        self.axes[0].set_title(
            f"{condition} - Vibration Signal"
        )

        self.axes[0].set_xlabel("Time (seconds)")
        self.axes[0].set_ylabel("Acceleration (g)")
        self.axes[0].grid(True)

        # Update FFT frequency spectrum

        frequencies = np.fft.rfftfreq(
            len(signal), d=0.01
        )

        spectrum = np.abs(np.fft.rfft(signal))

        self.axes[1].clear()
        self.axes[1].plot(frequencies, spectrum)

        self.axes[1].set_xlim(0, 25)

        self.axes[1].set_title(
            "Frequency Spectrum (FFT)"
        )

        self.axes[1].set_xlabel("Frequency (Hz)")
        self.axes[1].set_ylabel("FFT Amplitude")
        self.axes[1].grid(True)

        self.fig.tight_layout()
        self.canvas.draw()

        self.after_id = self.root.after(
            1000,
            self.update_dashboard
        )

    def show_history(self):

        history_window = tk.Toplevel(self.root)

        history_window.title(
            "EdgeGuard - Monitoring History"
        )

        history_window.geometry("1050x450")

        tk.Label(
            history_window,
            text="MOTOR MONITORING HISTORY",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        columns = (
            "ID",
            "Timestamp",
            "Selected",
            "Predicted",
            "RMS",
            "Peak"
        )

        table = ttk.Treeview(
            history_window,
            columns=columns,
            show="headings"
        )

        for column in columns:

            table.heading(
                column,
                text=column
            )

            table.column(
                column,
                width=150,
                anchor="center"
            )

        table.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        scrollbar = ttk.Scrollbar(
            history_window,
            orient="vertical",
            command=table.yview
        )

        table.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        records = get_all_readings()

        for record in records:

            table.insert(
                "",
                tk.END,
                values=(
                    record[0],
                    record[1],
                    record[2],
                    record[3],
                    f"{record[4]:.4f}",
                    f"{record[5]:.4f}"
                )
            )

        tk.Label(
            history_window,
            text=f"Total stored records: {len(records)}",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

    def export_history(self):

        records = get_all_readings()

        if not records:
            messagebox.showwarning(
                "No Records",
                "No monitoring records available!"
            )
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

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(records)

        messagebox.showinfo(
            "Export Successful",
            f"{len(records)} records exported successfully!\n\n"
            f"File: {filename}"
        )

    def show_analytics(self):

        records = get_all_readings()

        if not records:
            messagebox.showwarning(
                "No Data",
                "Start monitoring to collect readings first!"
            )
            return

        # Arrange records in chronological order

        records.reverse()

        rms_values = [row[4] for row in records]
        predictions = [row[3] for row in records]

        # Calculate fault distribution

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

        average_rms = sum(rms_values) / len(rms_values)

        # Create analytics window

        analytics_window = tk.Toplevel(self.root)

        analytics_window.title(
            "EdgeGuard - Historical Analytics"
        )

        analytics_window.geometry("1100x750")

        tk.Label(
            analytics_window,
            text="EDGEGUARD - HISTORICAL ANALYTICS",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        summary = (
            f"Total Records: {len(records)}     "
            f"Average RMS: {average_rms:.4f} g"
        )

        tk.Label(
            analytics_window,
            text=summary,
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        # Create charts

        fig, axes = plt.subplots(
            2, 1, figsize=(11, 8)
        )

        # RMS trend chart

        axes[0].plot(
            range(1, len(rms_values) + 1),
            rms_values,
            marker="o"
        )

        axes[0].set_title("Vibration RMS Trend")
        axes[0].set_xlabel("Reading Number")
        axes[0].set_ylabel("RMS (g)")
        axes[0].grid(True)

        # Fault distribution chart

        axes[1].bar(
            conditions,
            fault_counts
        )

        axes[1].set_title("Predicted Fault Distribution")
        axes[1].set_xlabel("Motor Condition")
        axes[1].set_ylabel("Number of Readings")
        axes[1].tick_params(
            axis="x",
            rotation=10
        )
        axes[1].grid(axis="y")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(
            fig,
            master=analytics_window
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

        def close_analytics():

            plt.close(fig)
            analytics_window.destroy()

        analytics_window.protocol(
            "WM_DELETE_WINDOW",
            close_analytics
        )

    def close_dashboard(self):

        self.stop_monitoring()
        self.root.destroy()


if __name__ == "__main__":

    root = tk.Tk()

    app = EdgeGuardDashboard(root)

    root.mainloop()