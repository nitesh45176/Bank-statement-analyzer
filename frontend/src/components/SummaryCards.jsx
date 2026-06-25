function SummaryCards({ summary }) {
  const cards = [
    {
      title: "Transactions",
      value: summary.total_transactions,
      accent: "border-l-indigo-500",
      valueClass: "text-indigo-600",
      sub: "this period",
    },
    {
      title: "Total Credits",
      value: `₹${summary.total_credit.toLocaleString()}`,
      accent: "border-l-emerald-500",
      valueClass: "text-emerald-600",
      sub: "inflow",
    },
    {
      title: "Total Debits",
      value: `₹${summary.total_debit.toLocaleString()}`,
      accent: "border-l-red-500",
      valueClass: "text-red-600",
      sub: "outflow",
    },
    {
      title: "Closing Balance",
      value: `₹${summary.closing_balance.toLocaleString()}`,
      accent: "border-l-amber-500",
      valueClass: "text-amber-600",
      sub: "end of period",
    },
  ];

  return (
    <div className="grid grid-cols-4 gap-3">
      {cards.map((card) => (
        <div
          key={card.title}
          className={`bg-white border border-slate-200 border-l-[3px] ${card.accent} rounded-xl p-5`}
        >
          <p className="text-[11px] font-medium uppercase tracking-widest text-slate-400 mb-2">
            {card.title}
          </p>
          <p className={`text-2xl font-bold leading-none ${card.valueClass}`}>
            {card.value}
          </p>
          <p className="text-[11px] text-slate-400 mt-1.5">{card.sub}</p>
        </div>
      ))}
    </div>
  );
}

export default SummaryCards;