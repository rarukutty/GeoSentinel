import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function TiltChart({ nodeId, refreshKey }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    if (!nodeId) return;

    fetch(`http://127.0.0.1:8000/api/history/${nodeId}`)
      .then((response) => response.json())
      .then((result) => setData(result))
      .catch((error) =>
        console.error("History API Error:", error)
      );
  }, [nodeId, refreshKey]);

  return (
    <div className="tilt-chart">

      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={data}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="timestamp"
            tick={{ fontSize: 10 }}
          />

          <YAxis
            label={{
              value: "Tilt (°)",
              angle: -90,
              position: "insideLeft",
            }}
          />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="tilt_magnitude"
            stroke="#22c55e"
            strokeWidth={2}
            dot={false}
          />

        </LineChart>
      </ResponsiveContainer>

    </div>
  );
}

export default TiltChart;