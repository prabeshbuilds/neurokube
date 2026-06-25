import type { InvestigationRecord } from "@/types";

interface HistoryTableProps {
  records: InvestigationRecord[];
  isLoading?: boolean;
}

export function HistoryTable({ records, isLoading }: HistoryTableProps) {
  return (
    <section className="panel p-6">
      <p className="panel-header">History</p>
      <h2 className="mt-1 text-lg font-semibold text-white">Recent Investigations</h2>

      {isLoading ? (
        <p className="mt-4 text-sm text-slate-500">Loading history...</p>
      ) : records.length === 0 ? (
        <p className="mt-4 rounded-lg border border-dashed border-slate-700 bg-slate-900/30 px-4 py-8 text-center text-sm text-slate-500">
          No completed investigations yet.
        </p>
      ) : (
        <div className="mt-4 overflow-x-auto rounded-lg border border-slate-800">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-900/80 text-slate-400">
                <th className="px-4 py-3 font-medium">Root Cause</th>
                <th className="px-4 py-3 font-medium">Cluster</th>
                <th className="px-4 py-3 font-medium">Namespace</th>
                <th className="px-4 py-3 font-medium">Confidence</th>
                <th className="px-4 py-3 font-medium">When</th>
              </tr>
            </thead>
            <tbody>
              {records.map((record, index) => (
                <tr
                  key={record.id}
                  className={`border-b border-slate-800/80 ${
                    index % 2 === 0 ? "bg-slate-900/20" : "bg-transparent"
                  }`}
                >
                  <td className="px-4 py-3 font-medium text-slate-200">
                    {record.root_cause ?? "—"}
                  </td>
                  <td className="px-4 py-3 text-slate-400">{record.cluster_context ?? "—"}</td>
                  <td className="px-4 py-3 text-slate-400">{record.namespace ?? "—"}</td>
                  <td className="px-4 py-3">
                    {record.confidence != null ? (
                      <span className="rounded-full bg-cyan-500/10 px-2 py-0.5 text-xs font-medium text-cyan-300">
                        {record.confidence}%
                      </span>
                    ) : (
                      "—"
                    )}
                  </td>
                  <td className="px-4 py-3 text-slate-500">
                    {new Date(record.created_at).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
