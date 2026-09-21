function DashboardStats({ nodes }) {

  const normal = nodes.filter(
    (node) => node.risk_level === "NORMAL"
  ).length;

  const warning = nodes.filter(
    (node) => node.risk_level === "WARNING"
  ).length;

  const high = nodes.filter(
    (node) => node.risk_level === "HIGH"
  ).length;

  const critical = nodes.filter(
    (node) => node.risk_level === "CRITICAL"
  ).length;

  return (
    <section className="stats">

      <div className="card">
        <h3>Total Nodes</h3>
        <strong>{nodes.length}</strong>
      </div>

      <div className="card normal-card">
        <h3>Normal</h3>
        <strong>{normal}</strong>
      </div>

      <div className="card warning-card">
        <h3>Warning</h3>
        <strong>{warning}</strong>
      </div>

      <div className="card high-card">
        <h3>High Risk</h3>
        <strong>{high}</strong>
      </div>

      <div className="card critical-card">
        <h3>Critical</h3>
        <strong>{critical}</strong>
      </div>

    </section>
  );
}

export default DashboardStats;