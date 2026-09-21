function RiskCard({ node }) {
  if (!node) {
    return (
      <div className="risk-card">
        <h2>Current Risk</h2>
        <p>Waiting for sensor data...</p>
      </div>
    );
  }

  return (
    <div className="risk-card">

      <div className="risk-card-header">
        <div>
          <h2>Current Risk</h2>
          <p>Latest monitoring status</p>
        </div>

        <div
          className="risk-indicator"
          style={{
            backgroundColor: node.risk_color,
            boxShadow: `0 0 20px ${node.risk_color}`,
          }}
        />
      </div>

      <div className="risk-level">
        {node.risk_level}
      </div>

      <div className="risk-details">

        <div>
          <span>Node</span>
          <strong>{node.node_id}</strong>
        </div>

        <div>
          <span>Tilt</span>
          <strong>{node.tilt_magnitude}°</strong>
        </div>

        <div>
          <span>Anomaly Score</span>
          <strong>{node.anomaly_score}</strong>
        </div>

      </div>

      <p className="risk-time">
        Last update: {node.timestamp}
      </p>

    </div>
  );
}

export default RiskCard;