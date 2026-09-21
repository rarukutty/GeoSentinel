import { useEffect, useState } from "react";

function EarlyWarnings({ refreshKey }) {

  const [alerts, setAlerts] = useState([]);

  useEffect(() => {

    fetch("http://127.0.0.1:8000/api/alerts")
      .then((response) => response.json())
      .then((data) => setAlerts(data))
      .catch((error) =>
        console.error("Alert API Error:", error)
      );

  }, [refreshKey]);


  return (
    <div className="early-warning">

      <div className="early-warning-header">

        <div>
          <h2>Early Warning</h2>

          <p>
            Deformation trend analysis
          </p>
        </div>

        <div className="warning-icon">
          ⚠️
        </div>

      </div>


      {alerts.length === 0 ? (

        <div className="warning-clear">
          🟢 No increasing deformation trends
        </div>

      ) : (

        <div className="warning-list">

          {alerts.map((alert) => (

            <div
              className="warning-item"
              key={alert.node_id}
            >

              <div className="warning-title">

                ⚠️ {alert.node_id} — Early Warning

              </div>

              <p>
                {alert.message}
              </p>

              <div className="warning-data">

                <span>
                  Current Tilt:
                  <strong>
                    {" "}
                    {alert.current_tilt}°
                  </strong>
                </span>

                <span>
                  Trend Increase:
                  <strong>
                    {" "}
                    +{alert.increase}°
                  </strong>
                </span>

              </div>

            </div>

          ))}

        </div>

      )}

    </div>
  );
}

export default EarlyWarnings;