import React from "react";
import { Bar, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

const Charts = ({ distribution }) => {
  if (!distribution || Object.keys(distribution).length === 0) return null;

  const labels = Object.keys(distribution);
  const values = Object.values(distribution);

  const barData = {
    labels,
    datasets: [
      {
        label: "Equipment Count",
        data: values,
        backgroundColor: "rgba(75,192,192,0.6)",
      },
    ],
  };

  const pieData = {
    labels,
    datasets: [
      {
        label: "Equipment Distribution",
        data: values,
        backgroundColor: [
          "#36A2EB",
          "#FF6384",
          "#FFCE56",
          "#4BC0C0",
          "#9966FF",
          "#FF9F40",
        ],
      },
    ],
  };

  return (
    <div className="w-4/5 mx-auto mt-8">
      <div className="mb-10">
        <Bar
          data={barData}
          options={{
            responsive: true,
            plugins: {
              title: { display: true, text: "Equipment Type Distribution (Bar)" },
            },
          }}
        />
      </div>
      <div>
        <Pie
          data={pieData}
          options={{
            responsive: true,
            plugins: {
              title: { display: true, text: "Equipment Type Distribution (Pie)" },
            },
          }}
        />
      </div>
    </div>
  );
};

export default Charts;
