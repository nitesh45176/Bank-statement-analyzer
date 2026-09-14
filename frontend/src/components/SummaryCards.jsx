import React from 'react';
import { Activity, ArrowUpRight, ArrowDownRight, Wallet, TrendingUp } from 'lucide-react';

const formatINR = (value) => {
  if (value === undefined || value === null) return '₹0';
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(value);
};

const Card = ({ title, value, icon: Icon, gradient, iconBg, iconColor, sub, badge }) => (
  <div className="relative bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md transition-all duration-300 hover:-translate-y-1 group">
    {/* Gradient accent bar */}
    <div className={`absolute top-0 left-0 right-0 h-1 ${gradient}`} />
    <div className="p-6">
      <div className="flex items-start justify-between mb-4">
        <div className={`p-2.5 rounded-xl ${iconBg}`}>
          <Icon className={`w-5 h-5 ${iconColor}`} strokeWidth={2.5} />
        </div>
        {badge && (
          <span className="text-[10px] font-semibold tracking-wider text-gray-400 uppercase bg-gray-50 px-2 py-1 rounded-md border border-gray-100">
            {badge}
          </span>
        )}
      </div>
      <p className="text-sm font-medium text-gray-500 mb-1">{title}</p>
      <p className="text-2xl font-bold text-gray-900 tracking-tight">{value}</p>
      {sub && <p className="text-xs text-gray-400 mt-1.5">{sub}</p>}
    </div>
  </div>
);

function SummaryCards({ summary }) {
  if (!summary) return null;

  const netFlow = (summary.total_credit || 0) - (summary.total_debit || 0);
  const isPositive = netFlow >= 0;

  const cards = [
    {
      title: 'Closing Balance',
      value: formatINR(summary.closing_balance),
      icon: Wallet,
      gradient: 'bg-gradient-to-r from-indigo-500 to-violet-500',
      iconBg: 'bg-indigo-50',
      iconColor: 'text-indigo-600',
      sub: 'End of statement period',
      badge: 'Balance',
    },
    {
      title: 'Total Income',
      value: formatINR(summary.total_credit),
      icon: ArrowUpRight,
      gradient: 'bg-gradient-to-r from-emerald-400 to-teal-500',
      iconBg: 'bg-emerald-50',
      iconColor: 'text-emerald-600',
      sub: 'Total credits this period',
      badge: 'Inflows',
    },
    {
      title: 'Total Spending',
      value: formatINR(summary.total_debit),
      icon: ArrowDownRight,
      gradient: 'bg-gradient-to-r from-rose-400 to-pink-500',
      iconBg: 'bg-rose-50',
      iconColor: 'text-rose-600',
      sub: 'Total debits this period',
      badge: 'Outflows',
    },
    {
      title: 'Net Cash Flow',
      value: formatINR(Math.abs(netFlow)),
      icon: isPositive ? TrendingUp : Activity,
      gradient: isPositive
        ? 'bg-gradient-to-r from-sky-400 to-blue-500'
        : 'bg-gradient-to-r from-amber-400 to-orange-500',
      iconBg: isPositive ? 'bg-sky-50' : 'bg-amber-50',
      iconColor: isPositive ? 'text-sky-600' : 'text-amber-600',
      sub: `${summary.total_transactions} transactions total`,
      badge: isPositive ? '▲ Positive' : '▼ Negative',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card) => (
        <Card key={card.title} {...card} />
      ))}
    </div>
  );
}

export default SummaryCards;