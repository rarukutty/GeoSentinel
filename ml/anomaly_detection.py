import pandas as pd
import numpy as np
from pathlib import Path


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned_tilt_data.csv"
OUTPUT_FILE = BASE_DIR / "data" / "anomaly_results.csv"


# --------------------------------------------------
# 2. Read cleaned data
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])

df = df.sort_values(["node_id", "timestamp"])


# --------------------------------------------------
# 3. Calculate tilt change
# --------------------------------------------------

df["tilt_change"] = (
    df.groupby("node_id")["tilt_magnitude"]
    .diff()
    .fillna(0)
)

df["abs_tilt_change"] = df["tilt_change"].abs()


# --------------------------------------------------
# 4. Calculate anomaly score
# --------------------------------------------------

df["anomaly_score"] = 0.0
df["anomaly"] = 0


for node in df["node_id"].unique():

    node_index = df["node_id"] == node

    node_data = df.loc[node_index].copy()

    values = node_data["tilt_magnitude"].values

    # Median
    median = np.median(values)

    # Median Absolute Deviation
    mad = np.median(np.abs(values - median))

    # Avoid division by zero
    if mad == 0:
        mad = 0.0001

    # Robust anomaly score
    scores = np.abs(values - median) / mad

    df.loc[node_index, "anomaly_score"] = scores

    # Score above 6 = anomaly
    df.loc[node_index, "anomaly"] = (
        scores > 6
    ).astype(int)


# --------------------------------------------------
# 5. Display results
# --------------------------------------------------

total_anomalies = int(df["anomaly"].sum())

print("Anomaly detection completed!")

print("\nTotal readings:", len(df))

print("Total anomalies detected:", total_anomalies)

print("\nAnomalies by node:")

print(
    df.groupby("node_id")["anomaly"].sum()
)


# --------------------------------------------------
# 6. Save results
# --------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\nResults saved to:")

print(OUTPUT_FILE)