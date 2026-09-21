import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# File locations
INPUT_FILE = BASE_DIR / "data" / "tilt_data.csv"
OUTPUT_FILE = BASE_DIR / "data" / "cleaned_tilt_data.csv"


# 1. Read the CSV file
df = pd.read_csv(INPUT_FILE)

print("Original data:")
print(df.head())

print("\nTotal rows:", len(df))


# 2. Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])


# 3. Check missing values
print("\nMissing values:")
print(df.isnull().sum())


# 4. Remove rows with missing values
df = df.dropna()


# 5. Remove duplicate rows
df = df.drop_duplicates()


# 6. Remove physically invalid tilt values
df = df[
    (df["tilt_x"].between(-90, 90)) &
    (df["tilt_y"].between(-90, 90))
]


# 7. Calculate overall tilt magnitude
df["tilt_magnitude"] = np.sqrt(
    df["tilt_x"] ** 2 + df["tilt_y"] ** 2
)


# 8. Sort data by node and time
df = df.sort_values(
    by=["node_id", "timestamp"]
)


# 9. Save cleaned data
df.to_csv(OUTPUT_FILE, index=False)


print("\nData cleaning completed!")
print("Cleaned rows:", len(df))
print("Saved to:", OUTPUT_FILE)


# 10. Display basic statistics
print("\nTilt statistics:")
print(df[["tilt_x", "tilt_y", "tilt_magnitude"]].describe())


# 11. Plot tilt magnitude for each node
plt.figure(figsize=(12, 6))

for node in df["node_id"].unique():

    node_data = df[df["node_id"] == node]

    plt.plot(
        node_data["timestamp"],
        node_data["tilt_magnitude"],
        label=node
    )


plt.title("Mine Subsidence - Tilt Trend")
plt.xlabel("Time")
plt.ylabel("Tilt Magnitude (degrees)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Save graph
graph_file = BASE_DIR / "data" / "tilt_trend.png"
plt.savefig(graph_file, dpi=150)

print("\nGraph saved to:", graph_file)

# Display graph
plt.show()