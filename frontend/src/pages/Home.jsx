import React, { useState } from "react";
import axios from "axios";
import Summary from "../components/Summary.jsx";

const baseURL = import.meta.env.VITE_API_BASE;
const username = import.meta.env.VITE_USERNAME;
const password = import.meta.env.VITE_PASSWORD;

const Home = () => {
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
      const res = await axios.post(`${baseURL}/upload/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        auth: {
          username,
          password,
        },
      });
      setSummary(res.data.summary || res.data);
      setError("");
    } catch (err) {
      setError("Upload failed. Check backend connection.");
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col items-center mt-10">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">
        Chemical Equipment Visualizer (Web)
      </h1>

      <div className="flex items-center gap-3 mb-4">
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
          className="block text-sm text-gray-700 
                     file:mr-4 file:py-2 file:px-4 
                     file:rounded-lg file:border-0 
                     file:text-sm file:font-semibold 
                     file:bg-blue-100 file:text-blue-700 
                     hover:file:bg-blue-200 
                     cursor-pointer"
        />

        <button
          onClick={handleUpload}
          className="px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Upload CSV
        </button>

        
      </div>

      {error && <p className="text-red-600 mt-2 font-medium">{error}</p>}

      <div className="mt-8 w-full max-w-4xl">
        <Summary summary={summary} />
      </div>
    </div>
  );
};

export default Home;
