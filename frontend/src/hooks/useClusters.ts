"use client";

import { useCallback, useEffect, useState } from "react";
import { fetchClusters } from "@/services/clusters";
import type { ClusterInfo } from "@/types";

export function useClusters(accessToken: string | null) {
  const [clusters, setClusters] = useState<ClusterInfo[]>([]);
  const [selectedCluster, setSelectedCluster] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!accessToken) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetchClusters(accessToken);
      if (response.error && response.clusters.length === 0) {
        setError(response.error);
        setClusters([]);
        return;
      }

      setClusters(response.clusters);
      if (response.error) {
        setError(response.error);
      }

      setSelectedCluster((current) => {
        if (current && response.clusters.some((cluster) => cluster.name === current)) {
          return current;
        }
        const currentCluster = response.clusters.find((cluster) => cluster.is_current);
        return currentCluster?.name ?? response.clusters[0]?.name ?? "";
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load clusters");
    } finally {
      setIsLoading(false);
    }
  }, [accessToken]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return {
    clusters,
    selectedCluster,
    setSelectedCluster,
    isLoading,
    error,
    refresh,
  };
}
