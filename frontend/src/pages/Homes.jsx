import { useState } from "react";
import CashoraHeader from "../components/CashoraHeader";
import UploadBox from "../components/UploadBox";
import SummaryCards from "../components/SummaryCards";
import FinancialCharts from "../components/FinancialCharts";
import SpendingInsights from "../components/SpendingInsights";
import TransactionTable from "../components/TransactionTable";
import ChatPanel from "../components/ChatPanel";

function Home() {
  const [data, setData] = useState(null);

  const handleExport = () => {
    if (data) {
      window.open(import.meta.env.VITE_API_URL + '/download' || 'http://localhost:8000/download', '_blank');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      <CashoraHeader 
        onUploadClick={() => setData(null)} 
        onExportClick={handleExport}
        isConnected={true} 
      />

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        
        <div className="mb-8 max-w-2xl">
          <UploadBox onUpload={setData} hasData={!!data} />
        </div>

        {data && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            
            {/* Top Level Insights */}
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 px-1">Financial Overview</h2>
              <SummaryCards summary={data.summary} />
            </section>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
              
              {/* Left Column (Charts & AI) */}
              <div className="xl:col-span-2 space-y-8">
                
                <section>
                  <FinancialCharts 
                    categoryData={data.category_summary}
                    monthlyData={data.monthly_summary}
                  />
                </section>

                <section>
                  <SpendingInsights insightsData={{
                    topCategory: { 
                      name: Object.keys(data.category_summary || {})[0] || 'N/A', 
                      amount: Object.values(data.category_summary || {})[0]?.debit || 0 
                    },
                    largestOutflow: data.top_debits && data.top_debits[0] ? {
                      merchant: data.top_debits[0].narration,
                      amount: data.top_debits[0].debit
                    } : null,
                    highestInflow: data.top_credits && data.top_credits[0] ? {
                      merchant: data.top_credits[0].narration,
                      amount: data.top_credits[0].credit
                    } : null,
                    netCashFlow: (data.summary?.total_credit || 0) - (data.summary?.total_debit || 0),
                    averageMonthlyOutflow: data.summary?.total_debit / Math.max(Object.keys(data.monthly_summary || {}).length, 1)
                  }} />
                </section>

                <section>
                  <TransactionTable transactions={data.transactions || []} />
                </section>

              </div>

              {/* Right Column (Cashora AI Assistant) */}
              <div className="xl:col-span-1">
                <div className="sticky top-24">
                  <ChatPanel statementId={data.statement_id} />
                </div>
              </div>

            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default Home;
