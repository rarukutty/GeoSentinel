function Alerts({ nodes }) {

  const alerts = nodes.filter(
    (node) =>
      node.risk_level === "HIGH" ||
      node.risk_level === "CRITICAL"
  );

  return (
    <div className="alerts">

      <div className="alerts-header">
        <div>
          <h2>Alerts</h2>
          <p>Potential ground movement detected</p>
        </div>

        <span className="alert-count">
          {alerts.length}
        </span>
      </div>

      {alerts.length === 0 ? (
        <div className="no-alert">
          🟢 No active alerts
        </div>
      ) : (
        <div className="alert-list">

          {alerts.map((node) => (
            <div
              className="alert-item"
              key={node.node_id}
            >

              <div
                className="alert-dot"
                style={{
                  backgroundColor: node.risk_color,
                }}
              />

              <div className="alert-content">

                <strong>
                  {node.node_id} — {node.risk_level}
                </strong>

                <p>
                  Tilt: {node.tilt_magnitude}°
                  {" • "}
                  Anomaly: {node.anomaly_score}
                </p>

              </div>

            </div>
          ))}

        </div>
      )}

    </div>
  );
}

export default Alerts;