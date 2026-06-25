import { apiClient } from "./api";
import type { ClusterListResponse } from "@/types";

export async function fetchClusters(accessToken: string): Promise<ClusterListResponse> {
  const response = await apiClient.get<ClusterListResponse>("/clusters", {
    headers: { Authorization: `Bearer ${accessToken}` },
    timeout: 15_000,
  });
  return response.data;
}
