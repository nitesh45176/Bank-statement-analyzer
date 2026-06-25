function MonthlyTable({ monthly }) {
  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-slate-50">
            {["Month", "Credits", "Debits", "Txns"].map((h, i) => (
              <th
                key={h}
                className={`text-[11px] font-semibold uppercase tracking-wider text-slate-400 px-5 py-2.5 border-b border-slate-100 ${i > 0 ? "text-right" : "text-left"}`}
              >
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Object.entries(monthly).map(([month, value], i) => (
            <tr key={month} className={i % 2 === 1 ? "bg-slate-50/60" : ""}>
              <td className="px-5 py-2.5 text-sm border-b border-slate-50">
                <span className="text-xs font-semibold text-blue-700 bg-blue-50 px-2.5 py-1 rounded">
                  {month}
                </span>
              </td>
              <td className="px-5 py-2.5 text-sm text-right text-emerald-600 font-medium border-b border-slate-50">
                ₹{value.credit.toLocaleString()}
              </td>
              <td className="px-5 py-2.5 text-sm text-right text-red-600 font-medium border-b border-slate-50">
                ₹{value.debit.toLocaleString()}
              </td>
              <td className="px-5 py-2.5 text-sm text-right text-slate-500 border-b border-slate-50">
                {value.count}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default MonthlyTable;