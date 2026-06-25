"use client";

import { InvestigateButton } from "@/components/InvestigateButton";
import { StatusBadge } from "@/components/StatusBadge";
import { useHealthCheck } from "@/hooks/useHealthCheck";
import { useInvestigate } from "@/hooks/useInvestigate";

export default function HomePage() {
  const { data: health, isLoading, isError } = useHealthCheck();
  const { investigate, isInvestigating } = useInvestigate();

  const statusLabel = isLoading
    ? "Checking..."
    : isError
      ? "Backend Unavailable"
      : health?.status === "healthy"
        ? "Ready"
        : "Unknown";

  return (
    <div className="flex min-h-full flex-1 items-center justify-center bg-slate-50 px-4">
      <main className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-10 text-center shadow-sm">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">
          AI Kubernetes Agent
        </h1>
        <p className="mt-3 text-base text-slate-600">
          Troubleshoot Kubernetes with AI
        </p>

        <div className="mt-8">
          <InvestigateButton
            onClick={investigate}
            disabled={isInvestigating || isError}
          />
        </div>

        <div className="mt-6 flex justify-center">
          <StatusBadge label={statusLabel} isLoading={isLoading} />
        </div>
      </main>
    </div>
  );
}
