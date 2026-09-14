import React from 'react';
import { ArrowUpRight, ArrowDownRight, Activity, CreditCard, PieChart } from 'lucide-react';

const formatINR = (value) => {
  if (value === undefined || value === null) return '₹0';
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(value);
};

const InsightCard = ({ title, value, icon: Icon, bgClass, textClass, subtitle }) => (
  <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 flex items-start gap-4 hover:shadow-md transition-all duration-200 hover:-translate-y-0.5">
    <div className={`p-3 rounded-xl ${bgClass} shrink-0`}>
      <Icon className={`w-5 h-5 ${textClass}`} strokeWidth={2.5} />
    </div>
    <div className="min-w-0">
      <p className="text-xs font-medium text-gray-400 uppercase tracking-wide truncate">{title}</p>
      <p className="text-xl font-bold text-gray-900 mt-1 truncate">{value}</p>
      {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
    </div>
  </div>
);

const SpendingInsights = ({ insightsData }) => {
  if (!insightsData) return null;

  const {
    topCategory,
    largestOutflow,
    netCashFlow,
    averageMonthlyOutflow
  } = insightsData;

  const isPositiveCashFlow = (netCashFlow || 0) >= 0;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <h2 className="text-base font-semibold text-gray-900">Spending Insights</h2>
        <span className="text-[10px] font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full border border-indigo-100">
          AI Computed
        </span>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <InsightCard
          title="Top Spending Category"
          value={topCategory?.name || 'N/A'}
          subtitle={topCategory ? `${formatINR(topCategory.amount)} total spend` : 'No data'}
          icon={PieChart}
          bgClass="bg-indigo-50"
          textClass="text-indigo-600"
        />
        <InsightCard
          title="Net Cash Flow"
          value={formatINR(Math.abs(netCashFlow || 0))}
          subtitle={isPositiveCashFlow ? '▲ Positive balance' : '▼ Negative balance'}
          icon={isPositiveCashFlow ? ArrowUpRight : ArrowDownRight}
          bgClass={isPositiveCashFlow ? 'bg-emerald-50' : 'bg-rose-50'}
          textClass={isPositiveCashFlow ? 'text-emerald-600' : 'text-rose-600'}
        />
        <InsightCard
          title="Largest Expense"
          value={formatINR(largestOutflow?.amount || 0)}
          subtitle={largestOutflow?.merchant || 'N/A'}
          icon={CreditCard}
          bgClass="bg-amber-50"
          textClass="text-amber-600"
        />
        <InsightCard
          title="Avg Monthly Outflow"
          value={formatINR(averageMonthlyOutflow || 0)}
          subtitle="Based on available months"
          icon={Activity}
          bgClass="bg-sky-50"
          textClass="text-sky-600"
        />
      </div>
    </div>
  );
};

export default SpendingInsights;
