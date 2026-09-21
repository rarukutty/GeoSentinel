from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Create FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="GeoSentinel API",
    description="Mine Subsidence Monitoring Backend",
    version="1.0"
)


# --------------------------------------------------
# 2. Allow React frontend to access the API
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# 3. Find risk results CSV
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "risk_results.csv"


# --------------------------------------------------
# 4. Basic home endpoint
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "project": "GeoSentinel",
        "status": "running",
        "message": "Mine Subsidence Monitoring API"
    }


# --------------------------------------------------
# 5. Get latest status of all nodes
# --------------------------------------------------

@app.get("/api/nodes")
def get_nodes():

    df = pd.read_csv(DATA_FILE)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Get latest reading for every node
    latest = (
        df.sort_values("timestamp")
        .groupby("node_id")
        .tail(1)
    )

    nodes = []

    for _, row in latest.iterrows():

        nodes.append({
            "node_id": row["node_id"],
            "timestamp": str(row["timestamp"]),
            "tilt_magnitude": round(
                float(row["tilt_magnitude"]), 4
            ),
            "anomaly": int(row["anomaly"]),
            "anomaly_score": round(
                float(row["anomaly_score"]), 4
            ),
            "risk_level": row["risk_level"],
            "risk_color": row["risk_color"]
        })

    return nodes


# --------------------------------------------------
# 6. Get data for one specific node
# --------------------------------------------------

@app.get("/api/nodes/{node_id}")
def get_node(node_id: str):

    df = pd.read_csv(DATA_FILE)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    node_data = df[
        df["node_id"].str.upper() == node_id.upper()
    ]

    if node_data.empty:

        return {
            "error": "Node not found"
        }

    # Return the latest reading
    latest = node_data.sort_values("timestamp").iloc[-1]

    return {
        "node_id": latest["node_id"],
        "timestamp": str(latest["timestamp"]),
        "tilt_magnitude": round(
            float(latest["tilt_magnitude"]), 4
        ),
        "anomaly": int(latest["anomaly"]),
        "anomaly_score": round(
            float(latest["anomaly_score"]), 4
        ),
        "risk_level": latest["risk_level"],
        "risk_color": latest["risk_color"]
    }
@app.get("/api/history/{node_id}")
def get_node_history(node_id: str):
    df = pd.read_csv(DATA_FILE)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    node_data = df[
        df["node_id"].str.upper() == node_id.upper()
    ].sort_values("timestamp")

    if node_data.empty:
        return {"error": "Node not found"}

    history = []

    for _, row in node_data.iterrows():
        history.append({
            "timestamp": str(row["timestamp"]),
            "tilt_magnitude": round(
                float(row["tilt_magnitude"]), 4
            ),
            "risk_level": row["risk_level"]
        })

    return history

@app.get("/api/alerts")
def get_alerts():

    df = pd.read_csv(DATA_FILE)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    alerts = []

    for node_id in df["node_id"].unique():

        node_data = (
            df[df["node_id"] == node_id]
            .sort_values("timestamp")
            .tail(10)
        )

        if len(node_data) < 5:
            continue

        # Calculate deformation trend
        first_value = node_data.iloc[0]["tilt_magnitude"]
        last_value = node_data.iloc[-1]["tilt_magnitude"]

        increase = last_value - first_value

        # Simple prototype trend rule
        if increase > 0.15:

            alerts.append({
                "node_id": node_id,
                "type": "EARLY_WARNING",
                "message": (
                    f"{node_id}: Ground deformation "
                    f"trend is increasing"
                ),
                "increase": round(float(increase), 4),
                "current_tilt": round(
                    float(last_value), 4
                ),
                "risk_level": node_data.iloc[-1]["risk_level"],
                "timestamp": str(
                    node_data.iloc[-1]["timestamp"]
                )
            })

    return alerts