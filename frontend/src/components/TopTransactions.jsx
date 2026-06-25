function TopTransactions({ title, transactions, type }) {
  const isCredit = type === "credit";

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-slate-100">
        <span className="text-sm font-semibold text-slate-800">{title}</span>
        <span
          className={`text-[11px] font-medium px-2.5 py-1 rounded-full ${
            isCredit
              ? "bg-emerald-50 text-emerald-700"
              : "bg-red-50 text-red-700"
          }`}
        >
          {isCredit ? "Inflows" : "Outflows"}
        </span>
      </div>
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-slate-50">
            {["Date", "Category", "Amount"].map((h, i) => (
              <th
                key={h}
                className={`text-[11px] font-semibold uppercase tracking-wider text-slate-400 px-5 py-2 border-b border-slate-100 ${i === 2 ? "text-right" : "text-left"}`}
              >
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {transactions.map((tx, i) => (
            <tr key={i} className={i % 2 === 1 ? "bg-slate-50/60" : ""}>
              <td className="px-5 py-2.5 text-xs text-slate-400 border-b border-slate-50">
                {tx.date}
              </td>
              <td className="px-5 py-2.5 text-xs text-slate-600 border-b border-slate-50">
                {tx.category}
              </td>
              <td
                className={`px-5 py-2.5 text-xs font-medium text-right border-b border-slate-50 ${
                  isCredit ? "text-emerald-600" : "text-red-600"
                }`}
              >
                ₹{tx.amount.toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TopTransactions;