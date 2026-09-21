import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "anomaly_results.csv"
OUTPUT_FILE = BASE_DIR / "data" / "risk_results.csv"


# --------------------------------------------------
# 2. Read anomaly results
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])


# --------------------------------------------------
# 3. Calculate risk level
# --------------------------------------------------

def calculate_risk(row):

    tilt = row["tilt_magnitude"]
    change = row["abs_tilt_change"]
    anomaly = row["anomaly"]

    # CRITICAL
    if anomaly == 1 and (tilt > 2.0 or change > 0.5):
        return "CRITICAL"

    # HIGH
    elif anomaly == 1 or tilt > 1.5:
        return "HIGH"

    # WARNING
    elif tilt > 1.0 or change > 0.15:
        return "WARNING"

    # NORMAL
    else:
        return "NORMAL"


df["risk_level"] = df.apply(calculate_risk, axis=1)


# --------------------------------------------------
# 4. Add risk color
# --------------------------------------------------

risk_colors = {
    "NORMAL": "GREEN",
    "WARNING": "YELLOW",
    "HIGH": "ORANGE",
    "CRITICAL": "RED"
}

df["risk_color"] = df["risk_level"].map(risk_colors)


# --------------------------------------------------
# 5. Display latest status of every node
# --------------------------------------------------

latest = (
    df.sort_values("timestamp")
    .groupby("node_id")
    .tail(1)
)

print("\n==============================")
print("CURRENT NODE RISK STATUS")
print("==============================")

for _, row in latest.iterrows():

    print(
        f"{row['node_id']} → "
        f"{row['risk_level']} "
        f"({row['risk_color']})"
    )


# --------------------------------------------------
# 6. Risk summary
# --------------------------------------------------

print("\n==============================")
print("RISK SUMMARY")
print("==============================")

print(
    df["risk_level"]
    .value_counts()
)


# --------------------------------------------------
# 7. Save results
# --------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\nRisk results saved to:")

print(OUTPUT_FILE)