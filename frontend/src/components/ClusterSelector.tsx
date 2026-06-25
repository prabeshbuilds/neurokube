import type { ClusterInfo } from "@/types";

interface ClusterSelectorProps {
  clusters: ClusterInfo[];
  selectedCluster: string;
  onSelect: (name: string) => void;
  isLoading?: boolean;
  error?: string | null;
}

export function ClusterSelector({
  clusters,
  selectedCluster,
  onSelect,
  isLoading,
  error,
}: ClusterSelectorProps) {
  if (isLoading) {
    return (
      <div className="panel p-6">
        <p className="panel-header">Clusters</p>
        <h2 className="mt-1 text-lg font-semibold text-white">Kubernetes Clusters</h2>
        <div className="mt-4 flex items-center gap-3 text-sm text-slate-400">
          <div className="h-4 w-4 animate-spin rounded-full border-2 border-cyan-500/30 border-t-cyan-400" />
          Loading clusters from kubeconfig...
        </div>
      </div>
    );
  }

  return (
    <section className="panel p-6">
      <p className="panel-header">Clusters</p>
      <h2 className="mt-1 text-lg font-semibold text-white">Kubernetes Clusters</h2>
      <p className="mt-1 text-sm text-slate-400">
        Select a cluster from your kubeconfig to investigate.
      </p>

      {error ? (
        <pre className="mt-4 whitespace-pre-wrap rounded-lg border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-sm text-amber-200">
          {error}
        </pre>
      ) : null}

      {clusters.length === 0 ? (
        <p className="mt-4 text-sm text-slate-500">No clusters found in kubeconfig.</p>
      ) : (
        <ul className="mt-4 grid gap-3 sm:grid-cols-2">
          {clusters.map((cluster) => {
            const selected = cluster.name === selectedCluster;
            return (
              <li key={cluster.name}>
                <button
                  type="button"
                  onClick={() => onSelect(cluster.name)}
                  className={`w-full rounded-xl border px-4 py-3.5 text-left transition-all duration-150 ${
                    selected
                      ? "border-cyan-500/60 bg-cyan-500/10 ring-1 ring-cyan-400/40 shadow-lg shadow-cyan-500/10"
                      : "border-slate-700/80 bg-slate-900/40 hover:border-slate-600 hover:bg-slate-800/50"
                  }`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-medium text-slate-100">{cluster.name}</span>
                    {cluster.is_current ? (
                      <span className="rounded-full bg-emerald-500/15 px-2 py-0.5 text-xs font-medium text-emerald-400 ring-1 ring-emerald-500/30">
                        current
                      </span>
                    ) : null}
                  </div>
                  <p className="mt-1.5 truncate font-mono text-xs text-slate-500">
                    {cluster.server}
                  </p>
                  <p className="mt-1 text-xs text-slate-600">
                    {cluster.cluster} · ns: {cluster.namespace}
                  </p>
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
