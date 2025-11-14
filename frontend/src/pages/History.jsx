import { useEffect, useState } from "react";
import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE;
const username = import.meta.env.VITE_USERNAME;
const password = import.meta.env.VITE_PASSWORD;
const History = () => {
  const [datasets, setDatasets] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        console.log(username, password , baseURL)
        const res = await axios.get(`${baseURL}/history/` ,{
          auth: {
          username: username,
          password: password,
          },
        });
        setDatasets(res.data);
      } catch (err) {
        console.error("Failed to load history:", err);
      }
    };
    fetchHistory();
  }, []);

  return (
    <div className="text-center mt-8">
      <h1 className="text-2xl font-semibold mb-6">Upload History (Last 5)</h1>
      <div className="overflow-x-auto">
        <table className="mx-auto w-4/5 border-collapse border border-gray-300 shadow-lg rounded-lg">
          <thead className="bg-gray-100">
            <tr>
              <th className="border border-gray-300 px-4 py-2 text-left">File Name</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Uploaded At</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Total Equipment</th>
              <th className="border border-gray-300 px-4 py-2 text-left">Download</th>
            </tr>
          </thead>
          <tbody>
            {datasets.map((d) => (
              <tr
                key={d.id}
                className="hover:bg-gray-50 transition-colors duration-200"
              >
                <td className="border border-gray-300 px-4 py-2">
                  {d.file.split("/").pop()}
                </td>
                <td className="border border-gray-300 px-4 py-2">
                  {new Date(d.uploaded_at).toLocaleString()}
                </td>
                <td className="border border-gray-300 px-4 py-2">
                  {d.summary?.total_equipment}
                </td>
                <td className="border border-gray-300 px-4 py-2">
                  <a
                    href={`${baseURL}/download/?id=${d.id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition"
                  >
                    Download
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default History;
