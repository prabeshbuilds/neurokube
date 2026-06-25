export function LoadingBanner() {
  return (
    <div className="panel flex items-start gap-4 border-cyan-500/25 bg-gradient-to-r from-cyan-500/10 to-teal-500/5 p-5">
      <div className="mt-0.5 h-5 w-5 shrink-0 animate-spin rounded-full border-2 border-cyan-500/30 border-t-cyan-400" />
      <div>
        <p className="text-sm font-semibold text-cyan-100">
          Investigating Kubernetes Cluster...
        </p>
        <p className="mt-1 text-sm text-slate-400">
          Collecting evidence and running AI reasoning. This may take a minute.
        </p>
      </div>
    </div>
  );
}
