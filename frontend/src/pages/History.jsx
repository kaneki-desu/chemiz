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
          username,
          password,
          },
        });
        setDatasets(res.data);
      } catch (err) {
        console.error("Failed to load history:", err);
      }
    };
    fetchHistory();
  }, []);

  const downloadPDF = async (id) => {
    try {
      const res = await axios.get(`${baseURL}/download/?id=${id}`, {
        auth: {
          username,
          password,
        },
        responseType: "blob",
      });

      // Create a download link
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = "equipment_summary.pdf";
      a.click();
      window.URL.revokeObjectURL(url);

    } catch (err) {
      console.error("Download failed:", err);
    }
  };

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
                  <button
                    onClick={() => downloadPDF(d.id)}
                    className="px-3 py-1 bg-green-600 text-white rounded">
                    Download
                  </button>

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
