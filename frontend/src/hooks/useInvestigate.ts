"use client";

import axios from "axios";
import { useState } from "react";
import { useAuth } from "@/lib/auth-context";
import { createInvestigation } from "@/services/history";
import { runInvestigation } from "@/services/investigate";
import type { Diagnosis } from "@/types";

function parseApiError(err: unknown): string {
  if (axios.isAxiosError(err)) {
    const detail = err.response?.data?.detail;
    if (typeof detail === "string") {
      return detail;
    }
    if (err.code === "ECONNABORTED") {
      return (
        "Investigation timed out.\n" +
        "The cluster or AI service may be slow. Please try again."
      );
    }
    if (!err.response) {
      return (
        "Unable to reach the backend API.\n" +
        "Please verify the backend is running at NEXT_PUBLIC_API_BASE_URL."
      );
    }
    return err.message;
  }
  if (err instanceof Error) {
    return err.message;
  }
  return "Investigation failed. Check backend and OpenRouter configuration.";
}

export function useInvestigate(clusterContext: string, onComplete?: () => void) {
  const { user, accessToken } = useAuth();
  const [isInvestigating, setIsInvestigating] = useState(false);
  const [investigationId, setInvestigationId] = useState<string | null>(null);
  const [diagnosis, setDiagnosis] = useState<Diagnosis | null>(null);
  const [clusterHealthy, setClusterHealthy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const investigate = async () => {
    if (!user?.id || !accessToken) {
      setError("You must be signed in to investigate");
      return;
    }

    if (!clusterContext) {
      setError("Please select a Kubernetes cluster before investigating.");
      return;
    }

    setIsInvestigating(true);
    setError(null);
    setDiagnosis(null);
    setClusterHealthy(false);

    try {
      const record = await createInvestigation(user.id);
      setInvestigationId(record.id);
      await new Promise((resolve) => setTimeout(resolve, 150));

      const result = await runInvestigation(record.id, clusterContext, accessToken);
      setDiagnosis(result.diagnosis);
      setClusterHealthy(result.cluster_healthy);
      onComplete?.();
    } catch (err) {
      setError(parseApiError(err));
    } finally {
      setIsInvestigating(false);
    }
  };

  return {
    investigate,
    isInvestigating,
    investigationId,
    diagnosis,
    clusterHealthy,
    error,
    clearError: () => setError(null),
  };
}
