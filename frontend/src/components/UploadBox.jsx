import { useState, useRef, useCallback } from "react";
import { UploadCloud, FileText, X, CheckCircle, Loader2 } from "lucide-react";
import api from "../api/helper";

const STEPS = [
  "Reading statement...",
  "Detecting bank format...",
  "Analyzing financial activity...",
  "Preparing Cashora AI...",
];

function UploadBox({ onUpload, hasStatement = false }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stepIndex, setStepIndex] = useState(0);
  const [dragging, setDragging] = useState(false);
  const fileInputRef = useRef(null);
  const stepTimerRef = useRef(null);

  const startStepCycle = () => {
    setStepIndex(0);
    let idx = 0;
    stepTimerRef.current = setInterval(() => {
      idx = (idx + 1) % STEPS.length;
      setStepIndex(idx);
    }, 1200);
  };

  const stopStepCycle = () => {
    if (stepTimerRef.current) {
      clearInterval(stepTimerRef.current);
      stepTimerRef.current = null;
    }
  };

  const handleFile = (selected) => {
    if (selected && selected.type === "application/pdf") {
      setFile(selected);
    } else if (selected) {
      alert("Please select a PDF file.");
    }
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragging(false);
    const dropped = e.dataTransfer.files[0];
    handleFile(dropped);
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setDragging(true);
  }, []);

  const handleDragLeave = useCallback(() => setDragging(false), []);

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    startStepCycle();

    try {
      const response = await api.post("/upload", formData);
      onUpload(response.data);
    } catch (error) {
      console.error(error);
      alert("Upload failed. Please check the file and try again.");
    } finally {
      stopStepCycle();
      setLoading(false);
    }
  };

  const clearFile = (e) => {
    e.stopPropagation();
    setFile(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const fileSizeLabel = (size) => {
    if (size >= 1024 * 1024) return `${(size / (1024 * 1024)).toFixed(1)} MB`;
    return `${(size / 1024).toFixed(0)} KB`;
  };

  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-6 pt-5 pb-4 border-b border-gray-100 flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-gray-900">
            {hasStatement ? "Replace Statement" : "Upload Statement"}
          </h2>
          <p className="text-xs text-gray-400 mt-0.5">
            Supports HDFC & PNB bank statement PDFs
          </p>
        </div>
        {hasStatement && (
          <span className="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-700 bg-emerald-50 border border-emerald-100 rounded-full px-3 py-1">
            <CheckCircle className="w-3.5 h-3.5" />
            Statement loaded
          </span>
        )}
      </div>

      <div className="p-6">
        {/* Drop Zone */}
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={() => !loading && fileInputRef.current?.click()}
          className={`relative flex flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed px-6 py-10 cursor-pointer transition-all duration-200 ${
            dragging
              ? "border-indigo-400 bg-indigo-50"
              : file
              ? "border-emerald-300 bg-emerald-50"
              : "border-gray-200 bg-gray-50 hover:border-indigo-300 hover:bg-indigo-50"
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            className="hidden"
            onChange={(e) => handleFile(e.target.files[0])}
          />

          {file ? (
            <>
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-100">
                <FileText className="w-6 h-6 text-emerald-600" />
              </div>
              <div className="text-center">
                <p className="text-sm font-semibold text-gray-800 truncate max-w-xs">
                  {file.name}
                </p>
                <p className="text-xs text-gray-400 mt-0.5">
                  {fileSizeLabel(file.size)} · PDF
                </p>
              </div>
              <button
                type="button"
                onClick={clearFile}
                className="absolute top-3 right-3 p-1 rounded-full bg-white border border-gray-200 text-gray-400 hover:text-rose-500 hover:border-rose-200 transition-colors"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </>
          ) : (
            <>
              <div className={`flex h-12 w-12 items-center justify-center rounded-xl transition-colors ${dragging ? "bg-indigo-100" : "bg-gray-100"}`}>
                <UploadCloud className={`w-6 h-6 transition-colors ${dragging ? "text-indigo-500" : "text-gray-400"}`} />
              </div>
              <div className="text-center">
                <p className="text-sm font-medium text-gray-700">
                  <span className="text-indigo-600 font-semibold">Click to upload</span> or drag & drop
                </p>
                <p className="text-xs text-gray-400 mt-1">PDF bank statement (HDFC, PNB)</p>
              </div>
            </>
          )}
        </div>

        {/* Action Row */}
        <div className="mt-4 flex items-center gap-3">
          {loading ? (
            <div className="flex-1 flex items-center gap-3 bg-indigo-50 rounded-xl px-4 py-3 border border-indigo-100">
              <Loader2 className="w-4 h-4 text-indigo-500 animate-spin shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-indigo-700 truncate">
                    {STEPS[stepIndex]}
                  </p>
                  <span className="text-xs text-indigo-400 ml-2 shrink-0">
                    Step {stepIndex + 1}/{STEPS.length}
                  </span>
                </div>
                <div className="mt-2 h-1.5 rounded-full bg-indigo-100 overflow-hidden">
                  <div
                    className="h-full bg-indigo-500 rounded-full transition-all duration-700"
                    style={{ width: `${((stepIndex + 1) / STEPS.length) * 100}%` }}
                  />
                </div>
              </div>
            </div>
          ) : (
            <button
              disabled={!file}
              onClick={uploadFile}
              className="flex-1 inline-flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-200 disabled:cursor-not-allowed text-white disabled:text-gray-400 rounded-xl px-5 py-3 text-sm font-semibold transition-all duration-200 shadow-sm hover:shadow-md"
            >
              <UploadCloud className="w-4 h-4" />
              {hasStatement ? "Replace & Analyze" : "Analyze Statement"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default UploadBox;