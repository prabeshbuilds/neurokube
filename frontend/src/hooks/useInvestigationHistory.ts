"use client";

import { useCallback, useEffect, useState } from "react";
import { fetchInvestigationHistory } from "@/services/history";
import type { InvestigationRecord } from "@/types";

export function useInvestigationHistory(userId: string | undefined) {
  const [history, setHistory] = useState<InvestigationRecord[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!userId) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const records = await fetchInvestigationHistory(userId);
      setHistory(records);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load history");
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { history, isLoading, error, refresh };
}
