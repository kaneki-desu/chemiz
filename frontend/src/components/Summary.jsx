import React from "react";
import Charts from "./Charts";

const Summary = ({ summary }) => {
  if (!summary) return null;

  return (
    <div className="mt-10 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold mb-4 text-gray-800">Summary</h2>
      <div className="space-y-2 text-gray-700">
        <p>
          <span className="font-medium">Total Equipments:</span> {summary.total_equipment}
        </p>
        <p>
          <span className="font-medium">Average Flowrate:</span> {summary.average_flowrate?.toFixed(2)}
        </p>
        <p>
          <span className="font-medium">Average Pressure:</span> {summary.average_pressure?.toFixed(2)}
        </p>
        <p>
          <span className="font-medium">Average Temperature:</span> {summary.average_temperature?.toFixed(2)}
        </p>
      </div>
      <div className="mt-6">
        <Charts distribution={summary.type_distribution} />
      </div>
    </div>
  );
};

export default Summary;
