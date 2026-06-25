import { useState } from "react";
import UploadBox from "../components/UploadBox";
import SummaryCards from "../components/SummaryCards";
import MonthlyTable from "../components/MonthlyTable";
import TopTransactions from "../components/TopTransactions";

function Home() {
  const [data, setData] = useState(null);

  return (
    <div className="min-h-screen bg-slate-100">
      {/* Header */}
      <header className="bg-blue-900 h-15 flex items-center gap-3 px-8 h-[60px]">
        <div className="w-7 h-7 bg-blue-600 rounded-md flex items-center justify-center flex-shrink-0">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="white"
            strokeWidth="1.8"
            className="w-4 h-4"
          >
            <rect x="3" y="8" width="18" height="13" rx="2" />
            <path d="M3 12h18" />
            <rect
              x="7"
              y="4"
              width="10"
              height="5"
              rx="1.5"
              fill="#93C5FD"
              stroke="none"
            />
          </svg>
        </div>
        <span className="text-white font-semibold text-sm tracking-wide">
          Statement Analyzer
        </span>
      </header>

      <div className="max-w-5xl mx-auto px-6 py-8">
        <UploadBox onUpload={setData} />

        {data && (
          <>
            {/* Section header with export */}
            <div className="flex items-center justify-between mt-7 mb-3">
              <span className="text-[11px] font-semibold tracking-widest uppercase text-slate-400">
                Overview
              </span>

              <a
                href="https://bank-statement-analyzer-x2z0.onrender.com/download"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 bg-white text-blue-700 border border-blue-200 rounded-lg px-3.5 py-1.5 text-xs font-medium hover:bg-blue-50 transition-colors"
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  className="w-3.5 h-3.5"
                >
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3" />
                </svg>
                Export Excel
              </a>
            </div>

            <SummaryCards summary={data.summary} />

            <p className="text-[11px] font-semibold tracking-widest uppercase text-slate-400 mt-7 mb-3">
              Monthly Breakdown
            </p>
            <MonthlyTable monthly={data.monthly_summary} />

            <div className="grid grid-cols-2 gap-4 mt-4">
              <TopTransactions
                title="Top Credits"
                transactions={data.top_credits}
                type="credit"
              />
              <TopTransactions
                title="Top Debits"
                transactions={data.top_debits}
                type="debit"
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Home;
