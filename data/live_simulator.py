import csv
import math
import random
import time
from datetime import datetime

from pathlib import Path


# --------------------------------------------------
# FILE LOCATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
RISK_FILE = BASE_DIR / "risk_results.csv"


# --------------------------------------------------
# NODE CONFIGURATION
# --------------------------------------------------

nodes = {
    "N01": {
        "tilt_x": 0.50,
        "tilt_y": 0.30
    },

    "N02": {
        "tilt_x": 0.50,
        "tilt_y": 0.30
    },

    "N03": {
        "tilt_x": 1.00,
        "tilt_y": 0.70
    },

    "N04": {
        "tilt_x": 0.55,
        "tilt_y": 0.36
    },

    "N05": {
        "tilt_x": 0.50,
        "tilt_y": 0.30
    }
}


# --------------------------------------------------
# LAST TILT VALUES
# --------------------------------------------------

previous_values = {
    node: {
        "tilt_x": values["tilt_x"],
        "tilt_y": values["tilt_y"]
    }
    for node, values in nodes.items()
}


# --------------------------------------------------
# CALCULATE RISK
# --------------------------------------------------

def calculate_risk(tilt, change):

    if tilt > 2.0 or change > 0.5:
        return "CRITICAL", "#ef4444"

    elif tilt > 1.5 or change > 0.25:
        return "HIGH", "#f97316"

    elif tilt > 1.0 or change > 0.15:
        return "WARNING", "#eab308"

    else:
        return "NORMAL", "#22c55e"


# --------------------------------------------------
# ADD ONE READING
# --------------------------------------------------

def generate_reading(node_id):

    current = nodes[node_id]

    # Small natural sensor noise
    noise_x = random.uniform(-0.02, 0.02)
    noise_y = random.uniform(-0.02, 0.02)

    # --------------------------------------------------
    # NORMAL NODES
    # --------------------------------------------------

    if node_id in ["N01", "N02", "N05"]:

        current["tilt_x"] += noise_x
        current["tilt_y"] += noise_y


    # --------------------------------------------------
    # N03 = GRADUAL DEFORMATION
    # --------------------------------------------------

    elif node_id == "N03":

        current["tilt_x"] += 0.015 + noise_x
        current["tilt_y"] += 0.010 + noise_y


    # --------------------------------------------------
    # N04 = RAPID DEFORMATION
    # --------------------------------------------------

    elif node_id == "N04":

        current["tilt_x"] += 0.035 + noise_x
        current["tilt_y"] += 0.025 + noise_y


    tilt_x = current["tilt_x"]
    tilt_y = current["tilt_y"]


    # --------------------------------------------------
    # TILT MAGNITUDE
    # --------------------------------------------------

    tilt_magnitude = math.sqrt(
        tilt_x ** 2 + tilt_y ** 2
    )


    # --------------------------------------------------
    # CHANGE FROM PREVIOUS READING
    # --------------------------------------------------

    previous = previous_values[node_id]

    previous_magnitude = math.sqrt(
        previous["tilt_x"] ** 2 +
        previous["tilt_y"] ** 2
    )

    tilt_change = abs(
        tilt_magnitude - previous_magnitude
    )


    # --------------------------------------------------
    # DEMO ANOMALY SCORE
    # --------------------------------------------------

    anomaly_score = round(
        tilt_change * 10,
        4
    )

    anomaly = 1 if (
        tilt_change > 0.05 or
        tilt_magnitude > 1.5
    ) else 0


    # --------------------------------------------------
    # RISK
    # --------------------------------------------------

    risk_level, risk_color = calculate_risk(
        tilt_magnitude,
        tilt_change
    )


    # Update previous values

    previous_values[node_id] = {
        "tilt_x": tilt_x,
        "tilt_y": tilt_y
    }


    return {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "node_id": node_id,

        "tilt_x": round(tilt_x, 4),

        "tilt_y": round(tilt_y, 4),

        "tilt_magnitude": round(
            tilt_magnitude,
            4
        ),

        "tilt_change": round(
            tilt_change,
            4
        ),

        "abs_tilt_change": round(
            tilt_change,
            4
        ),

        "anomaly_score": anomaly_score,

        "anomaly": anomaly,

        "risk_level": risk_level,

        "risk_color": risk_color
    }


# --------------------------------------------------
# APPEND TO CSV
# --------------------------------------------------

def save_reading(reading):

    file_exists = RISK_FILE.exists()

    fieldnames = [
        "timestamp",
        "node_id",
        "tilt_x",
        "tilt_y",
        "tilt_magnitude",
        "tilt_change",
        "abs_tilt_change",
        "anomaly_score",
        "anomaly",
        "risk_level",
        "risk_color"
    ]

    with open(
        RISK_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(reading)


# --------------------------------------------------
# MAIN LIVE LOOP
# --------------------------------------------------

print("======================================")
print(" GeoSentinel Live Sensor Simulator")
print("======================================")

print("")

print("Simulating:")

print("N01 → Normal")
print("N02 → Normal")
print("N03 → Gradual deformation")
print("N04 → Progressive deformation")
print("N05 → Normal")

print("")

print("New readings every 5 seconds...")
print("Press CTRL+C to stop.")

print("")


while True:

    print(
        f"\n[{datetime.now().strftime('%H:%M:%S')}]"
    )

    for node_id in nodes:

        reading = generate_reading(node_id)

        save_reading(reading)

        print(
            f"{node_id} | "
            f"Tilt: {reading['tilt_magnitude']}° | "
            f"Risk: {reading['risk_level']}"
        )


    time.sleep(5)