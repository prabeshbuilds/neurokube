import { INVESTIGATION_STEPS } from "@/types";

interface ProgressListProps {
  completedSteps: string[];
  isActive: boolean;
}

export function ProgressList({ completedSteps, isActive }: ProgressListProps) {
  return (
    <section className="panel p-6">
      <p className="panel-header">Live Progress</p>
      <h2 className="mt-1 text-lg font-semibold text-white">Investigation Status</h2>
      {isActive ? (
        <p className="mt-2 flex items-center gap-2 text-sm text-cyan-300/90">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-cyan-400 opacity-60" />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-cyan-400" />
          </span>
          Investigating Kubernetes Cluster...
        </p>
      ) : null}
      <ul className="mt-5 space-y-2.5">
        {INVESTIGATION_STEPS.map(({ step, label }) => {
          const done = completedSteps.includes(step);
          const pending = isActive && !done;

          return (
            <li
              key={step}
              className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors ${
                done
                  ? "bg-emerald-500/10 text-emerald-300"
                  : pending
                    ? "bg-cyan-500/5 text-slate-200"
                    : "text-slate-600"
              }`}
            >
              <span
                className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold ${
                  done
                    ? "bg-emerald-500/20 text-emerald-400"
                    : pending
                      ? "bg-cyan-500/20 text-cyan-400"
                      : "bg-slate-800 text-slate-600"
                }`}
              >
                {done ? "✓" : pending ? "…" : "○"}
              </span>
              <span>{label}</span>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
