"use client";

import { AuthGuard } from "@/components/AuthGuard";
import { BrandLogo } from "@/components/BrandLogo";
import { ClusterSelector } from "@/components/ClusterSelector";
import { DiagnosisCard } from "@/components/DiagnosisCard";
import { ErrorAlert } from "@/components/ErrorAlert";
import { HealthyClusterBanner } from "@/components/HealthyClusterBanner";
import { HistoryTable } from "@/components/HistoryTable";
import { InvestigateButton } from "@/components/InvestigateButton";
import { LoadingBanner } from "@/components/LoadingBanner";
import { ProgressList } from "@/components/ProgressList";
import { useClusters } from "@/hooks/useClusters";
import { useInvestigate } from "@/hooks/useInvestigate";
import { useInvestigationHistory } from "@/hooks/useInvestigationHistory";
import { useInvestigationRealtime } from "@/hooks/useInvestigationRealtime";
import { useAuth } from "@/lib/auth-context";
import { APP_TAGLINE } from "@/lib/brand";
import { INVESTIGATION_STEPS } from "@/types";

function DashboardContent() {
  const { user, accessToken, signOut } = useAuth();
  const {
    clusters,
    selectedCluster,
    setSelectedCluster,
    isLoading: clustersLoading,
    error: clustersError,
  } = useClusters(accessToken);

  const { history, isLoading: historyLoading, refresh } = useInvestigationHistory(
    user?.id,
  );

  const {
    investigate,
    isInvestigating,
    investigationId,
    diagnosis,
    clusterHealthy,
    error,
  } = useInvestigate(selectedCluster, refresh);

  const { completedSteps } = useInvestigationRealtime(investigationId, isInvestigating);

  const displayCompleted = diagnosis
    ? INVESTIGATION_STEPS.map((step) => step.step)
    : completedSteps;

  const showHealthy = Boolean(diagnosis && clusterHealthy);
  const showDiagnosis = Boolean(diagnosis && !clusterHealthy);

  return (
    <div className="app-shell min-h-full">
      <header className="sticky top-0 z-10 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
          <BrandLogo showTagline />
          <div className="flex items-center gap-4">
            <p className="hidden text-sm text-slate-400 sm:block">{user?.email}</p>
            <button type="button" onClick={() => signOut()} className="btn-ghost">
              Sign Out
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl space-y-6 px-4 py-8 sm:px-6">
        <div className="panel border-cyan-500/20 bg-gradient-to-r from-cyan-500/5 to-teal-500/5 p-6">
          <p className="panel-header">Operations Console</p>
          <h2 className="mt-2 text-2xl font-semibold tracking-tight text-white">
            Cluster Investigation
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-slate-400">
            {APP_TAGLINE}. Select a cluster, collect evidence, and receive AI-guided
            root cause analysis with actionable fixes.
          </p>
        </div>

        <ClusterSelector
          clusters={clusters}
          selectedCluster={selectedCluster}
          onSelect={setSelectedCluster}
          isLoading={clustersLoading}
          error={clustersError}
        />

        <section className="panel p-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="panel-header">Run Investigation</p>
              <h2 className="mt-1 text-lg font-semibold text-white">Start Scan</h2>
              <p className="mt-1 text-sm text-slate-400">
                {selectedCluster
                  ? `Target cluster: ${selectedCluster}`
                  : "Select a cluster above to begin."}
              </p>
            </div>
            <InvestigateButton
              onClick={investigate}
              disabled={isInvestigating || !selectedCluster}
            />
          </div>
          {error ? (
            <div className="mt-4">
              <ErrorAlert message={error} />
            </div>
          ) : null}
        </section>

        {isInvestigating ? <LoadingBanner /> : null}

        {(isInvestigating || displayCompleted.length > 0) && (
          <ProgressList completedSteps={displayCompleted} isActive={isInvestigating} />
        )}

        {showHealthy ? (
          <HealthyClusterBanner clusterContext={selectedCluster} />
        ) : null}

        {showDiagnosis && diagnosis ? <DiagnosisCard diagnosis={diagnosis} /> : null}

        <HistoryTable records={history} isLoading={historyLoading} />
      </main>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <AuthGuard>
      <DashboardContent />
    </AuthGuard>
  );
}
