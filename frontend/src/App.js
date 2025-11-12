import React, { useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setError("Please upload a CSV file!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(`${process.env.REACT_APP_API_BASE}/upload/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSummary(res.data.summary);
      console.log(res.data);
      setError("");
    } catch (err) {
      setError("Upload failed. Check backend connection.");
      console.error(err);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: 30 }}>
      <h1>Chemical Equipment Visualizer (Web)</h1>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
        style={{ marginRight: 10 }}
      />
      <button onClick={handleUpload}>Upload CSV</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Render summary only if valid */}
      {summary && Object.keys(summary).length > 0 && (
        <div style={{ marginTop: 40 }}>
          <h2>Summary</h2>
          <p>Total Equipments: {summary.total_count}</p>

          {summary.averages && (
            <>
              <p>Average Flowrate: {summary.averages.Flowrate?.toFixed(2)}</p>
              <p>Average Pressure: {summary.averages.Pressure?.toFixed(2)}</p>
              <p>Average Temperature: {summary.averages.Temperature?.toFixed(2)}</p>
            </>
          )}

          {/* Only render chart if type_distribution exists */}
          {summary.type_distribution && (
            <div style={{ width: "60%", margin: "auto" }}>
              <Bar
                data={{
                  labels: Object.keys(summary.type_distribution || {}),
                  datasets: [
                    {
                      label: "Equipment Type Count",
                      data: Object.values(summary.type_distribution || {}),
                      backgroundColor: "rgba(75, 192, 192, 0.6)",
                    },
                  ],
                }}
                options={{
                  responsive: true,
                  plugins: {
                    legend: { position: "top" },
                    title: { display: true, text: "Equipment Type Distribution" },
                  },
                }}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
