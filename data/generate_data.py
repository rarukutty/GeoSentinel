import pandas as pd
import numpy as np

# Make results reproducible
np.random.seed(42)

# Settings
nodes = ["N01", "N02", "N03", "N04", "N05"]
readings_per_node = 288

# Create timestamps at 5-minute intervals
timestamps = pd.date_range(
    start="2026-09-01 00:00:00",
    periods=readings_per_node,
    freq="5min"
)

data = []

for node in nodes:

    for i, timestamp in enumerate(timestamps):

        # Normal sensor noise
        tilt_x = np.random.normal(0.5, 0.05)
        tilt_y = np.random.normal(0.3, 0.05)

        # N03: gradual ground deformation
        if node == "N03":
            tilt_x += i * 0.003
            tilt_y += i * 0.002

        # N04: sudden abnormal movement
        if node == "N04" and i > 240:
            tilt_x += (i - 240) * 0.08
            tilt_y += (i - 240) * 0.05

        data.append([
            timestamp,
            node,
            round(tilt_x, 4),
            round(tilt_y, 4)
        ])

# Convert to DataFrame
df = pd.DataFrame(
    data,
    columns=["timestamp", "node_id", "tilt_x", "tilt_y"]
)

# Save CSV
df.to_csv("data/tilt_data.csv", index=False)

print("Sensor data generated successfully!")
print(f"Total readings: {len(df)}")
print(df.head())