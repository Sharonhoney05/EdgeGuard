import tkinter as tk
from tkinter import ttk
from collections import deque
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# EDGEGUARD - Advanced Motor Monitoring Dashboard
# Data source: SIMULATED vibration readings

root = tk.Tk()
root.title("EdgeGuard - Advanced Motor Monitoring")
root.geometry("1100x800")
root.configure(bg="#17212b")

samples_x = deque(maxlen=100)
samples_y = deque(maxlen=100)
samples_z = deque(maxlen=100)

sample_count = 0
time_step = 0
running = True
history_counter = 0

# ---------------- HEADER ----------------

tk.Label(
    root,
    text="EDGEGUARD",
    font=("Arial", 25, "bold"),
    fg="white",
    bg="#17212b"
).pack(pady=(12, 2))

tk.Label(
    root,
    text="ADVANCED MOTOR CONDITION MONITORING | SIMULATED DATA",
    font=("Arial", 10),
    fg="#b8c7d9",
    bg="#17212b"
).pack(pady=4)

# ---------------- STATUS ----------------

status_frame = tk.Frame(root, bg="#263746", padx=15, pady=10)
status_frame.pack(fill="x", padx=20, pady=10)

status_label = tk.Label(
    status_frame,
    text="MOTOR STATUS: STARTING",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#263746"
)
status_label.pack()

alert_label = tk.Label(
    status_frame,
    text="Waiting for readings...",
    font=("Arial", 11),
    fg="#b8c7d9",
    bg="#263746"
)
alert_label.pack(pady=5)

# ---------------- MEASUREMENT CARDS ----------------

cards = tk.Frame(root, bg="#17212b")
cards.pack(fill="x", padx=15, pady=8)

def create_card(parent, title, initial):
    frame = tk.Frame(parent, bg="#263746", padx=8, pady=10)
    frame.pack(side="left", expand=True, fill="x", padx=4)

    tk.Label(
        frame,
        text=title,
        font=("Arial", 10, "bold"),
        fg="#b8c7d9",
        bg="#263746"
    ).pack()

    value = tk.Label(
        frame,
        text=initial,
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#263746"
    )
    value.pack(pady=5)

    return value

rms_value = create_card(cards, "VIBRATION RMS", "0.000 g")
peak_value = create_card(cards, "PEAK VIBRATION", "0.000 g")
x_value = create_card(cards, "X ACCELERATION", "0.000 g")
y_value = create_card(cards, "Y ACCELERATION", "0.000 g")
z_value = create_card(cards, "Z ACCELERATION", "1.000 g")

# ---------------- GRAPH ----------------

figure, axis = plt.subplots(figsize=(9, 3))
figure.patch.set_facecolor("#17212b")
axis.set_facecolor("#263746")

axis.set_title("Live Vibration Waveform", color="white")
axis.set_xlabel("Sample Number", color="white")
axis.set_ylabel("Acceleration (g)", color="white")
axis.tick_params(colors="white")
axis.grid(True, alpha=0.25)

line_x, = axis.plot([], [], label="X axis")
line_y, = axis.plot([], [], label="Y axis")
line_z, = axis.plot([], [], label="Z axis")

legend = axis.legend()
for text_item in legend.get_texts():
    text_item.set_color("white")

figure.tight_layout()

canvas = FigureCanvasTkAgg(figure, master=root)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=5)

# ---------------- HISTORY TABLE ----------------

history_title = tk.Label(
    root,
    text="MOTOR MONITORING HISTORY",
    font=("Arial", 12, "bold"),
    fg="white",
    bg="#17212b"
)
history_title.pack(pady=(5, 3))

table_frame = tk.Frame(root)
table_frame.pack(fill="x", padx=20, pady=5)

columns = ("Sample", "RMS (g)", "Peak (g)", "Condition")

history_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=4
)

for column in columns:
    history_table.heading(column, text=column)
    history_table.column(column, anchor="center", width=150)

history_table.pack(fill="x")

# ---------------- BUTTONS ----------------

button_frame = tk.Frame(root, bg="#17212b")
button_frame.pack(pady=10)

# ---------------- MONITORING FUNCTION ----------------

def update_dashboard():

    global sample_count, time_step, history_counter

    if not running:
        return

    # Three simulated motor conditions
    phase = (sample_count // 100) % 3

    if phase == 0:
        amplitude = 0.02
    elif phase == 1:
        amplitude = 0.15
    else:
        amplitude = 0.40

    # Simulated three-axis acceleration
    x = amplitude * math.sin(time_step * 0.5)
    y = amplitude * 0.7 * math.sin(time_step * 0.5 + 1)
    z = 1.0 + amplitude * 0.5 * math.sin(time_step * 0.5 + 2)

    # Small measurement noise
    x += random.uniform(-0.002, 0.002)
    y += random.uniform(-0.002, 0.002)
    z += random.uniform(-0.002, 0.002)

    samples_x.append(x)
    samples_y.append(y)
    samples_z.append(z)

    sample_count += 1
    time_step += 1

    # Remove average offset from each axis
    dx = np.array(samples_x) - np.mean(samples_x)
    dy = np.array(samples_y) - np.mean(samples_y)
    dz = np.array(samples_z) - np.mean(samples_z)

    # Combined three-axis vibration RMS
    vibration_magnitude_squared = dx**2 + dy**2 + dz**2
    rms = float(np.sqrt(np.mean(vibration_magnitude_squared)))

    # Peak vibration magnitude
    peak = float(np.max(np.sqrt(vibration_magnitude_squared)))

    # Preliminary demonstration thresholds
    if rms < 0.05:
        condition = "NORMAL"
        status_color = "#239b56"
        alert = "Motor operating normally"
    elif rms < 0.20:
        condition = "WARNING"
        status_color = "#d68910"
        alert = "Warning: Increased vibration detected"
    else:
        condition = "ABNORMAL"
        status_color = "#c0392b"
        alert = "Alert: Abnormal vibration detected!"

    # Update status and alert
    status_label.config(
        text=f"MOTOR STATUS: {condition}",
        fg=status_color
    )

    alert_label.config(
        text=alert,
        fg=status_color
    )

    # Update measurement cards
    rms_value.config(text=f"{rms:.4f} g")
    peak_value.config(text=f"{peak:.4f} g")
    x_value.config(text=f"{x:.4f} g")
    y_value.config(text=f"{y:.4f} g")
    z_value.config(text=f"{z:.4f} g")

    # Update graph
    line_x.set_data(range(len(samples_x)), samples_x)
    line_y.set_data(range(len(samples_y)), samples_y)
    line_z.set_data(range(len(samples_z)), samples_z)

    axis.set_xlim(0, 100)
    axis.set_ylim(-0.5, 1.5)

    canvas.draw_idle()

    # Add a history entry every 10 samples
    history_counter += 1

    if history_counter >= 10:
        history_table.insert(
            "",
            "end",
            values=(
                sample_count,
                f"{rms:.4f}",
                f"{peak:.4f}",
                condition
            )
        )

        # Keep the latest 10 history entries
        rows = history_table.get_children()

        if len(rows) > 10:
            history_table.delete(rows[0])

        history_counter = 0

    root.after(100, update_dashboard)


# ---------------- START / STOP ----------------

def start_monitoring():
    global running

    if not running:
        running = True
        update_dashboard()


def stop_monitoring():
    global running
    running = False

    status_label.config(
        text="MONITORING STOPPED",
        fg="#b8c7d9"
    )

    alert_label.config(
        text="Monitoring paused",
        fg="#b8c7d9"
    )


start_button = tk.Button(
    button_frame,
    text="START MONITORING",
    command=start_monitoring,
    bg="#239b56",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=8
)
start_button.pack(side="left", padx=10)

stop_button = tk.Button(
    button_frame,
    text="STOP MONITORING",
    command=stop_monitoring,
    bg="#c0392b",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=8
)
stop_button.pack(side="left", padx=10)

update_dashboard()

root.mainloop()