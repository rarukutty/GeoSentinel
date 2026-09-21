function RiskMap({ nodes }) {
  return (
    <div className="risk-map">
      <div className="map-grid">

        {nodes.map((node, index) => (
          <div
            key={node.node_id}
            className="map-node"
            style={{
              left: `${15 + (index % 3) * 35}%`,
              top: `${20 + Math.floor(index / 3) * 45}%`,
            }}
          >
            <div
              className="node-dot"
              style={{
                backgroundColor: node.risk_color,
                boxShadow: `0 0 15px ${node.risk_color}`,
              }}
            />

            <span>{node.node_id}</span>
          </div>
        ))}

      </div>
    </div>
  );
}

export default RiskMap;