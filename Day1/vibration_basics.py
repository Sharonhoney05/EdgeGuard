import math

# Normal motor vibration readings
normal = [1, -1, 2, -2, 1, -1, 2, -2]

# Abnormal motor vibration readings
abnormal = [5, -5, 6, -6, 5, -5, 6, -6]


# Function to calculate RMS
def calculate_rms(readings):
    squared_values = [x ** 2 for x in readings]

    mean = sum(squared_values) / len(squared_values)

    rms = math.sqrt(mean)

    return rms


# Calculate vibration levels
normal_rms = calculate_rms(normal)
abnormal_rms = calculate_rms(abnormal)

print("EDGEGUARD MOTOR MONITORING")
print("--------------------------")

print("Normal Motor RMS:", normal_rms)
print("Abnormal Motor RMS:", abnormal_rms)

if abnormal_rms > normal_rms:
    print("Warning: Higher vibration detected!")