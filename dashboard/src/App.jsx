import { useEffect, useState } from "react";
import "./App.css";
import RiskMap from "./components/RiskMap";
import TiltChart from "./components/TiltChart";
import RiskCard from "./components/RiskCard";
import Alerts from "./components/Alerts";
import EarlyWarnings from "./components/EarlyWarnings";
import DashboardStats from "./components/DashboardStats";

function App() {
  const [nodes, setNodes] = useState([]);
const [selectedNode, setSelectedNode] = useState("N04");
const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {

  const fetchNodes = () => {
    fetch("http://127.0.0.1:8000/api/nodes")
      .then((response) => response.json())
      .then((data) => {
        setNodes(data);
        setRefreshKey((value) => value + 1);
      })
      .catch((error) =>
        console.error("API Error:", error)
      );
  };

  // Fetch immediately
  fetchNodes();

  // Refresh every 5 seconds
  const interval = setInterval(fetchNodes, 5000);

  // Cleanup when component is removed
  return () => clearInterval(interval);

}, []);

   return (
    <div className="dashboard">

      <header>

  <div className="header-top">

    <div>
      <h1>GeoSentinel</h1>

      <p>
        AI-Powered Mine Subsidence Monitoring System
      </p>
    </div>

    <div className="system-info">

      <div className="live-status">
        <span className="live-dot"></span>
        LIVE
      </div>

      <span>
        Backend: <strong>ONLINE</strong>
      </span>

      <span>
        Refresh: <strong>5 sec</strong>
      </span>

    </div>

  </div>

</header>

     <DashboardStats nodes={nodes} />
      <section className="map-section">

  <div className="section-header">
    <div>
      <h2>Mine Risk Map</h2>
      <p>Real-time simulated ground monitoring</p>
    </div>

    <div className="legend">
      <span>🟢 Normal</span>
      <span>🟡 Warning</span>
      <span>🟠 High</span>
      <span>🔴 Critical</span>
    </div>
  </div>

  <RiskMap nodes={nodes} />

</section>
<section className="chart-section">

  <div className="section-header">

    <div>
      <h2>Historical Tilt Trend</h2>
      <p>
        Ground deformation over time — {selectedNode}
      </p>
    </div>

    <select
      className="node-selector"
      value={selectedNode}
      onChange={(event) =>
        setSelectedNode(event.target.value)
      }
    >

      <option value="N01">N01</option>
      <option value="N02">N02</option>
      <option value="N03">N03</option>
      <option value="N04">N04</option>
      <option value="N05">N05</option>

    </select>

  </div>

  <TiltChart
    nodeId={selectedNode}
    refreshKey={refreshKey}
  />

</section>
<section className="bottom-grid">

  <RiskCard
    node={nodes.find(
      (node) => node.risk_level === "CRITICAL"
    ) || nodes[0]}
  />

  <Alerts nodes={nodes} />

</section>
<EarlyWarnings refreshKey={refreshKey} />

      <section className="node-section">
        <h2>Node Status</h2>

        <div className="node-grid">
          {nodes.map((node) => (
            <div
              className="node-card"
              key={node.node_id}
            >
              <h3>{node.node_id}</h3>

              <p>
                Tilt: {node.tilt_magnitude}°
              </p>

              <p>
                Anomaly Score: {node.anomaly_score}
              </p>

              <div
                className="risk"
                style={{ backgroundColor: node.risk_color }}
              >
                {node.risk_level}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;