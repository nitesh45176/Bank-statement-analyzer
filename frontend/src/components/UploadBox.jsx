import { useState } from "react";
import api from "../api/helper";

function UploadBox({ onUpload }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadFile = async () => {
    if (!file) return alert("Please select a PDF.");
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);
    try {
      const response = await api.post("/upload", formData);
      onUpload(response.data);
    } catch (error) {
      console.error(error);
      alert("Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-7 flex items-center gap-5">
      <label className="flex-1 flex items-center gap-4 border-[1.5px] border-dashed border-slate-300 rounded-lg px-5 py-4 bg-slate-50 cursor-pointer hover:border-blue-400 hover:bg-blue-50 transition-colors">
        <div className="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center flex-shrink-0">
          <svg viewBox="0 0 24 24" fill="none" stroke="#2563EB" strokeWidth="1.8" className="w-5 h-5">
            <path d="M14 3v4a1 1 0 001 1h4" />
            <path d="M17 21H7a2 2 0 01-2-2V5a2 2 0 012-2h7l5 5v11a2 2 0 01-2 2z" />
            <path d="M12 11v6M9 14l3-3 3 3" />
          </svg>
        </div>
        <div>
          <p className="text-sm font-medium text-slate-700">
            {file ? file.name : <><span className="text-blue-600">Choose a PDF</span> or drag it here</>}
          </p>
          <p className="text-xs text-slate-400 mt-0.5">
            {file ? `${(file.size / 1024).toFixed(0)} KB` : "Bank statement in PDF format"}
          </p>
        </div>
        <input
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </label>

      <button
        disabled={loading}
        onClick={uploadFile}
        className="inline-flex items-center gap-2 bg-blue-800 hover:bg-blue-900 disabled:opacity-60 text-white rounded-lg px-5 py-2.5 text-sm font-medium transition-colors whitespace-nowrap"
      >
        {loading ? (
          <>
            <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4" />
            </svg>
            Analyzing…
          </>
        ) : (
          <>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-4 h-4">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
            Analyze
          </>
        )}
      </button>
    </div>
  );
}

export default UploadBox;