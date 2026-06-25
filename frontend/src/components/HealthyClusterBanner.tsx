interface HealthyClusterBannerProps {
  clusterContext: string;
}

export function HealthyClusterBanner({ clusterContext }: HealthyClusterBannerProps) {
  return (
    <section className="panel border-emerald-500/25 bg-gradient-to-br from-emerald-500/10 to-teal-500/5 p-6">
      <div className="flex items-start gap-4">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-400 ring-1 ring-emerald-500/30">
          ✓
        </div>
        <div>
          <p className="panel-header text-emerald-400/90">All Clear</p>
          <h2 className="mt-1 text-lg font-semibold text-emerald-100">
            No critical Kubernetes issues detected
          </h2>
          <p className="mt-2 text-sm text-emerald-200/80">
            Cluster <strong className="text-emerald-100">{clusterContext}</strong> appears
            healthy.
          </p>
          <p className="mt-2 text-sm text-slate-400">
            Deploy a test scenario from{" "}
            <code className="rounded bg-slate-900/60 px-1.5 py-0.5 font-mono text-xs text-cyan-300/90">
              k8s/test-scenarios/
            </code>{" "}
            to validate failure detection.
          </p>
        </div>
      </div>
    </section>
  );
}
